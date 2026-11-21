from django.apps import AppConfig


class FossAccessConfig(AppConfig):
    name = "posthog.foss_access"
    # The access-control models shipped in the FOSS tree retain this historical Django app label.
    label = "ee"
