# Daily ceilings on created tasks (trailing 24h) on top of the in-flight cap: a workflow
# triggered by a common event can otherwise sustain hundreds of agent runs a day through
# the concurrency cap alone. The team cap aggregates across a team's workflows so N
# workflows can't each spend the per-workflow cap; it is deliberately separate from the
# loops budget (LOOP_RATE_CAP_PER_DAY / LOOP_TEAM_RATE_CAP_PER_DAY).
WORKFLOW_TASK_RATE_CAP_PER_DAY = 100
WORKFLOW_TASK_TEAM_RATE_CAP_PER_DAY = 500

# A project raises either cap for itself in project settings, up to this multiple of the
# default. The ceiling is held by the team API serializer, so support can still take a
# project past it in Django admin, which does not use that serializer.
WORKFLOW_TASK_RATE_CAP_SELF_SERVE_MULTIPLIER = 5
MAX_SELF_SERVE_WORKFLOW_TASK_RATE_CAP_PER_DAY = (
    WORKFLOW_TASK_RATE_CAP_PER_DAY * WORKFLOW_TASK_RATE_CAP_SELF_SERVE_MULTIPLIER
)
MAX_SELF_SERVE_WORKFLOW_TASK_TEAM_RATE_CAP_PER_DAY = (
    WORKFLOW_TASK_TEAM_RATE_CAP_PER_DAY * WORKFLOW_TASK_RATE_CAP_SELF_SERVE_MULTIPLIER
)
