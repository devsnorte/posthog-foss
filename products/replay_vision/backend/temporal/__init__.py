"""Load worker registrations only when a caller requests them."""

from importlib import import_module
from typing import Any


def __getattr__(name: str) -> Any:
    if name not in __all__:
        raise AttributeError(name)
    return getattr(import_module(f"{__name__}.registry"), name)


__all__ = [
    "ACTIVITIES",
    "WORKFLOWS",
    "ApplyScannerWorkflow",
    "BackfillScannerWorkflow",
    "MeterScannerReadsWorkflow",
    "ObservationMediaWorkflow",
    "ReconcileScannerSchedulesWorkflow",
    "RefreshScannerEstimatesWorkflow",
    "RefreshLearnedRulesWorkflow",
    "ReplayVisionGeminiCleanupSweepWorkflow",
    "SweepScannerWorkflow",
    "advance_scanner_watermark_activity",
    "call_scanner_provider_activity",
    "cleanup_gemini_file_activity",
    "create_observation_activity",
    "delete_scanner_schedule_activity",
    "embed_observation_activity",
    "emit_classifier_tags_activity",
    "emit_observation_event_activity",
    "complete_observation_requests_activity",
    "emit_observation_signal_summaries_activity",
    "ensure_session_asset_activity",
    "fetch_session_events_activity",
    "fetch_session_network_activity",
    "sweep_scanner_tick_activity",
    "finalize_observation_activity",
    "prepare_observation_activity",
    "list_enabled_scanners_activity",
    "list_scanner_schedules_activity",
    "list_stale_scanner_estimates_activity",
    "meter_scanner_read_bytes_activity",
    "mark_observation_failed_activity",
    "mark_observation_ineligible_activity",
    "mark_observation_running_activity",
    "mark_observation_succeeded_activity",
    "reap_childless_inline_scanners_activity",
    "reap_orphaned_observations_activity",
    "refresh_scanner_estimate_activity",
    "start_launched_scanners_activity",
    "sweep_gemini_files_activity",
    "upload_video_to_gemini_activity",
    "upsert_scanner_schedule_activity",
]
