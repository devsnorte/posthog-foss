from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

from posthog.models import Organization, Team

from products.signals.backend.quota import prepare_self_driving_admission
from products.signals.backend.trial.billing import TrialContinuation, trial_billing_status
from products.signals.backend.trial.funding import TrialFunding
from products.signals.backend.trial.policy import TrialRefused


@override_settings(EE_AVAILABLE=False, DEBUG=True)
class TestFossAdmission(SimpleTestCase):
    def test_new_work_requires_a_funding_source(self):
        team = Team(id=1, organization=Organization(name="test"))
        self.assertEqual(trial_billing_status(team).continuation, TrialContinuation.UNAVAILABLE)
        with patch("products.signals.backend.trial.policy.TrialPolicy.admission_grant", return_value=None):
            admission = prepare_self_driving_admission(team)
        with self.assertRaises(TrialRefused) as error:
            admission.bind()
        self.assertEqual(error.exception.reason, "billing_unavailable")

    def test_child_work_keeps_its_accepted_funding(self):
        team = Team(id=1, organization=Organization(name="test"))
        funding = TrialFunding(funding="operator")
        admission = prepare_self_driving_admission(team, parent=funding)
        self.assertFalse(admission.gate.enforced)
        self.assertIs(admission.parent, funding)
