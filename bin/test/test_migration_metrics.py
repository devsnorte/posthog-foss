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
            for address in (None, "", "gateway:9091"):
                for code in (0, 1):
                    with self.subTest(address=address, code=code):
                        env = {
                            "PATH": tmp + os.pathsep + os.defpath,
                            "MIGRATE_CODE": str(code),
                            "MIGRATE_MAX_RETRIES": "1",
                        }
                        if address is not None:
                            env["PROM_PUSHGATEWAY_ADDRESS"] = address
                        result = subprocess.run([MIGRATE, "--scope=postgres"], env=env, capture_output=True, text=True)
                        self.assertEqual(result.returncode, code, result.stderr)
                        reports = [
                            line
                            for line in result.stdout.splitlines()
                            if line.startswith("manage.py report_migration_metric ")
                        ]
                        self.assertEqual(len(reports), int(bool(address)))
                        if reports:
                            args = reports[0].split()
                            self.assertIn("--attempts=1", args)
                            self.assertTrue(any(arg.startswith("--duration=") for arg in args))
                            self.assertEqual("--success" in args, code == 0)
