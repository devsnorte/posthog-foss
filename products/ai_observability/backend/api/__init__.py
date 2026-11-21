"""Import endpoint implementations on demand so metrics can load independently."""

from importlib import import_module
from typing import Any

_VIEW_MODULES = {
    "AIBlobViewSet": "ai_blob",
    "ClusteringConfigViewSet": "clustering_config",
    "ClusteringJobViewSet": "clustering_job",
    "AIObservabilityClusteringRunViewSet": "clustering",
    "AIObservabilityInstrumentationChecklistViewSet": "instrumentation_checklist",
    "LLMModelsViewSet": "models",
    "LLMProxyViewSet": "proxy",
    "AIObservabilityTextReprViewSet": "text_repr",
    "AIObservabilitySummarizationViewSet": "summarization",
    "AIObservabilityTranslateViewSet": "translate",
    "SUPPORTED_MODELS_WITH_THINKING": "proxy",
    "DatasetViewSet": "datasets",
    "DatasetItemViewSet": "datasets",
    "EvaluationViewSet": "evaluations",
    "EvalSuggestionViewSet": "eval_suggestions",
    "EvaluationBackfillViewSet": "evaluation_backfills",
    "EvaluationDirectoryViewSet": "evaluation_directories",
    "EvaluationReportViewSet": "evaluation_reports",
    "EvaluationRunViewSet": "evaluation_runs",
    "EvaluationConfigViewSet": "evaluation_config",
    "LLMProviderKeyViewSet": "provider_keys",
    "LLMProviderKeyValidationViewSet": "provider_keys",
    "ReviewQueueViewSet": "review_queues",
    "ReviewQueueItemViewSet": "review_queues",
    "ScoreDefinitionViewSet": "score_definitions",
    "OfflineExperimentViewSet": "offline_experiments",
    "OfflineScorerViewSet": "offline_experiment_reads",
    "PersonalSpendInternalViewSet": "personal_spend",
    "PersonalSpendViewSet": "personal_spend",
    "TaggerViewSet": "taggers",
    "TraceReviewViewSet": "trace_reviews",
    "ParserRecipeViewSet": "parser_recipes",
}

__all__ = list(_VIEW_MODULES)


def __getattr__(name: str) -> Any:
    if name not in _VIEW_MODULES:
        raise AttributeError(name)
    return getattr(import_module(f"{__name__}.{_VIEW_MODULES[name]}"), name)
