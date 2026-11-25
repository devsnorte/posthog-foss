from django.conf import settings


def access_schema_dependency(migration: str) -> tuple[str, str]:
    """Resolve historical access-schema dependencies for the installed edition."""
    if settings.EE_AVAILABLE:
        return ("ee", migration)
    if migration in {"0069_squash_2026_11_02_finalize_fks", "0070_squash_2026_11_02_schema_addons"}:
        return ("ee", "0002_feature_flag_role_access")
    return ("ee", "0001_foss_access")
