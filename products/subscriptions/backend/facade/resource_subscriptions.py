"""Subscription lookups and cleanup used by the resources being delivered."""

from __future__ import annotations

from collections.abc import Collection
from datetime import datetime

from products.subscriptions.backend.logic import queries
from products.subscriptions.backend.models.subscription import Subscription

from . import contracts


def failed_delivery_counts(*, team_id: int, since: datetime, limit: int) -> list[contracts.FailedDeliveryCount]:
    """Subscriptions that failed to deliver since `since`, most failures first. Deleted subscriptions are left out."""
    return queries.failed_delivery_counts(team_id=team_id, since=since, limit=limit)


def subscription_ids_in_team(*, team_id: int, subscription_ids: Collection[int]) -> set[int]:
    """Which of the given subscription ids belong to the team."""
    return queries.subscription_ids_in_team(team_id=team_id, subscription_ids=subscription_ids)


def insight_short_ids_subscribed_by(*, team_id: int, user_id: int, email: str, now: datetime, limit: int) -> list[str]:
    """Short ids of insights in active subscriptions the user receives, newest subscription first.

    Email subscriptions match the user's address among the recipients. Slack and Teams
    subscriptions have no person recipient, so they match the user who created them.
    """
    return queries.insight_short_ids_subscribed_by(team_id=team_id, user_id=user_id, email=email, now=now, limit=limit)


def user_has_slack_subscription(*, team_id: int, user_id: int) -> bool:
    """Whether the user created a subscription that delivers to Slack in this team. A disabled one counts."""
    return queries.user_has_slack_subscription(team_id=team_id, user_id=user_id)


def delete_insight_subscriptions(*, project_id: int, insight_ids: Collection[int]) -> None:
    # nosemgrep: environment-model-scoped-by-project -- insights are project-level, so deleting one removes its subscriptions in every environment
    for subscription in Subscription.objects.filter(team__project_id=project_id, insight_id__in=insight_ids):
        subscription.delete()


def insight_ids_with_subscriptions(insight_ids: Collection[int]) -> set[int]:
    """Which of the given insights have a subscription that has not been deleted.

    Paused subscriptions (enabled=False) count: disabling delivery does not withdraw the intent
    to deliver this insight again.
    """
    # Caller-supplied ids that are already team-scoped by the caller's own query; this only maps
    # ids to ids and returns no row data.
    # nosemgrep: idor-lookup-without-team
    return set(
        Subscription.objects.filter(insight_id__in=insight_ids, deleted=False).values_list("insight_id", flat=True)
    )


def dashboard_ids_with_subscriptions(dashboard_ids: Collection[int]) -> set[int]:
    """Which of the given dashboards have a subscription that has not been deleted.

    Paused subscriptions (enabled=False) count: disabling delivery does not withdraw the intent
    to deliver this dashboard again.
    """
    # Caller-supplied ids that are already team-scoped by the caller's own query; this only maps
    # ids to ids and returns no row data.
    # nosemgrep: idor-lookup-without-team
    return set(
        Subscription.objects.filter(dashboard_id__in=dashboard_ids, deleted=False).values_list(
            "dashboard_id", flat=True
        )
    )


def insight_has_active_subscription(insight_id: int) -> bool:
    """Whether an enabled subscription delivers this insight, directly or as a dashboard tile."""
    return queries.insight_has_active_subscription(insight_id)


def insight_ids_with_active_subscriptions(*, team_ids: Collection[int]) -> set[int]:
    """Insights of these teams that an enabled subscription delivers, directly or as a live dashboard tile."""
    return queries.insight_ids_with_active_subscriptions(team_ids=team_ids)


def dashboard_has_active_full_subscription(dashboard_id: int) -> bool:
    """Whether an enabled subscription delivers every insight on this dashboard."""
    return queries.dashboard_has_active_full_subscription(dashboard_id)
