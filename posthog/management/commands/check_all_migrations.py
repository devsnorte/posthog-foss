from io import StringIO

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Check PostgreSQL, ClickHouse, and async migrations in startup order."
    requires_system_checks = []

    def handle(self, *args, **options):
        try:
            call_command("migrate", "--check", skip_checks=False)
        except SystemExit as error:
            if error.code:
                plan = StringIO()
                call_command("showmigrations", "--plan", stdout=plan, skip_checks=False)
                pending = [line[4:] for line in plan.getvalue().splitlines() if line.startswith("[ ] ")]
                if pending:
                    self.stdout.write(
                        f"The local database lacks these migrations, so this is local state, not a migration conflict: {' '.join(pending)}"
                    )
                    self.stdout.write("Run 'hogli migrations:up' to apply them.")
            raise

        call_command("migrate_clickhouse", "--check", skip_checks=False)
        call_command("run_async_migrations", "--check", skip_checks=False)
