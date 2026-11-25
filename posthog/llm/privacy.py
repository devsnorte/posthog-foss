from typing import TYPE_CHECKING

from django.conf import settings

if TYPE_CHECKING:
    from posthog.models import Team

if settings.EE_AVAILABLE:
    from ee.hogai.utils.feature_flags import is_privacy_mode_enabled as is_privacy_mode_enabled
else:

    def is_privacy_mode_enabled(team: "Team") -> bool:
        # Without the remote privacy setting, omit customer content from AI telemetry.
        return True
