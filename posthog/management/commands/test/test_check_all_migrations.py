from io import StringIO

from unittest import TestCase
from unittest.mock import patch

from posthog.management.commands.check_all_migrations import Command


class TestStartupChecks(TestCase):
    def test_pending_migration_stops_subsequent_checks(self):
        def run(name, *args, **options):
            if name == "migrate":
                raise SystemExit(1)
            self.assertEqual(name, "showmigrations")
            options["stdout"].write("[X] app.applied\n[ ] app.pending\n")

        output = StringIO()
        with patch("posthog.management.commands.check_all_migrations.call_command", side_effect=run):
            with self.assertRaises(SystemExit) as error:
                Command(stdout=output).handle()
        self.assertEqual(error.exception.code, 1)
        self.assertIn("app.pending", output.getvalue())
        self.assertNotIn("app.applied", output.getvalue())

    def test_clickhouse_failure_stops_async_check(self):
        with patch(
            "posthog.management.commands.check_all_migrations.call_command", side_effect=[None, SystemExit(1)]
        ) as run:
            with self.assertRaises(SystemExit):
                Command().handle()
        self.assertEqual(
            [c.args for c in run.call_args_list], [("migrate", "--check"), ("migrate_clickhouse", "--check")]
        )
