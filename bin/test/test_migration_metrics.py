import os
import tempfile
import subprocess
from pathlib import Path

import unittest

MIGRATE = Path(__file__).resolve().parents[1] / "migrate"


class TestMigrationMetrics(unittest.TestCase):
    def test_optional_reporter_preserves_migration_result(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            python = Path(tmp) / "python"
            python.write_text(
                "#!/bin/sh\n"
                'echo "$@"\n'
                'case "$2" in\n'
                '    migrate) exit "$MIGRATE_CODE" ;;\n'
                "    report_migration_metric) exit 1 ;;\n"
                "esac\n"
            )
            python.chmod(0o755)
            for settings, expect_report in [
                ({}, False),
                ({"PROM_PUSHGATEWAY_ADDRESS": ""}, False),
                ({"PROM_PUSHGATEWAY_ADDRESS": "gateway:9091"}, True),
                ({"DJANGO_SETTINGS_MODULE": "custom.settings"}, True),
            ]:
                for code in (0, 1):
                    with self.subTest(settings=settings, code=code):
                        env = {
                            "PATH": tmp + os.pathsep + os.defpath,
                            "MIGRATE_CODE": str(code),
                            "MIGRATE_MAX_RETRIES": "1",
                            **settings,
                        }
                        result = subprocess.run([MIGRATE, "--scope=postgres"], env=env, capture_output=True, text=True)
                        self.assertEqual(result.returncode, code, result.stderr)
                        reports = [
                            line
                            for line in result.stdout.splitlines()
                            if line.startswith("manage.py report_migration_metric ")
                        ]
                        self.assertEqual(len(reports), int(expect_report))
                        if reports:
                            args = reports[0].split()
                            self.assertIn("--attempts=1", args)
                            self.assertTrue(any(arg.startswith("--duration=") for arg in args))
                            self.assertEqual("--success" in args, code == 0)
