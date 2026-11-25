// Must stay the first import, so that no dependency runs before the prototypes are sealed. The import order in
// .prettierrc keeps it first.
import '~/common/utils/seal-intrinsics'

// NOTE: Keep these as ~ imports as we can validate the build output this way
import { PluginServerMode } from '~/common/config'
import { defaultConfig, overrideConfigWithEnv } from '~/common/config/config'
import { initMetrics } from '~/common/metrics/otel-metrics'
import { initTracing } from '~/common/tracing/otel'
import { initSuperProperties } from '~/common/utils/posthog'
import { getDefaultIngestionConsumerConfig } from '~/ingestion/config'
import type { NodeServer } from '~/servers/base-server'

async function createServer(): Promise<NodeServer> {
    const { PLUGIN_SERVER_EVENTS_INGESTION_PIPELINE } = overrideConfigWithEnv(getDefaultIngestionConsumerConfig())
    initSuperProperties(PLUGIN_SERVER_EVENTS_INGESTION_PIPELINE)

    switch (defaultConfig.PLUGIN_SERVER_MODE) {
        case PluginServerMode.ingestion_v2:
        case PluginServerMode.ingestion_v2_combined: {
            const { IngestionGeneralServer } = await import('./servers/ingestion-general-server.js')
            return new IngestionGeneralServer()
        }

        case PluginServerMode.ingestion_api: {
            const { IngestionApiServer } = await import('./servers/ingestion-api-server.js')
            return new IngestionApiServer()
        }

        case PluginServerMode.recordings_blob_ingestion_v2:
        case PluginServerMode.recordings_blob_ingestion_v2_overflow: {
            const { IngestionSessionReplayServer } = await import('./servers/ingestion-session-replay-server.js')
            return new IngestionSessionReplayServer()
        }

        case PluginServerMode.recordings_blob_ingestion_v2_ml_mirror: {
            const { IngestionSessionReplayMlMirrorServer } = await import('./servers/ingestion-session-replay-ml-mirror-server.js')
            return new IngestionSessionReplayMlMirrorServer()
        }

        case PluginServerMode.recordings_blob_ingestion_v2_ml_parquet_sink: {
            const { IngestionSessionReplayMlParquetSinkServer } = await import('./servers/ingestion-session-replay-ml-parquet-sink-server.js')
            return new IngestionSessionReplayMlParquetSinkServer()
        }

        case PluginServerMode.recordings_blob_ingestion_v2_ml_image_scrub: {
            const { IngestionSessionReplayMlImageScrubServer } = await import('./servers/ingestion-session-replay-ml-image-scrub-server.js')
            return new IngestionSessionReplayMlImageScrubServer()
        }

        case PluginServerMode.recordings_blob_ingestion_v2_ml_image_scrub_dlq_replay: {
            const { IngestionSessionReplayMlImageScrubDlqReplayServer } = await import('./servers/ingestion-session-replay-ml-image-scrub-dlq-replay-server.js')
            return new IngestionSessionReplayMlImageScrubDlqReplayServer()
        }

        case PluginServerMode.recordings_blob_ingestion_v2_ml_image_fetch: {
            const { IngestionSessionReplayMlImageFetchServer } = await import('./servers/ingestion-session-replay-ml-image-fetch-server.js')
            return new IngestionSessionReplayMlImageFetchServer()
        }

        case PluginServerMode.recordings_blob_ingestion_v2_ml_image_fetch_retry: {
            const { IngestionSessionReplayMlImageFetchRetryServer } = await import('./servers/ingestion-session-replay-ml-image-fetch-retry-server.js')
            return new IngestionSessionReplayMlImageFetchRetryServer()
        }

        case PluginServerMode.ai_research_v4_image_fetch: {
            const { AiResearchV4ImageFetchServer } = await import('./servers/ai-research-v4-image-fetch-server.js')
            return new AiResearchV4ImageFetchServer()
        }

        case PluginServerMode.ai_research_v4_image_fetch_retry: {
            const { AiResearchV4ImageFetchRetryServer } = await import('./servers/ai-research-v4-image-fetch-server.js')
            return new AiResearchV4ImageFetchRetryServer()
        }

        case PluginServerMode.recording_api: {
            const { RecordingApiServer } = await import('./servers/recording-api-server.js')
            return new RecordingApiServer()
        }

        case PluginServerMode.ingestion_error_tracking: {
            const { ErrorTrackingServer } = await import('./servers/error-tracking-server.js')
            return new ErrorTrackingServer()
        }

        case PluginServerMode.ingestion_logs: {
            const { IngestionLogsServer } = await import('./servers/ingestion-logs-server.js')
            return new IngestionLogsServer()
        }

        case PluginServerMode.ingestion_metrics: {
            const { IngestionMetricsServer } = await import('./servers/ingestion-metrics-server.js')
            return new IngestionMetricsServer()
        }

        case PluginServerMode.ingestion_traces: {
            const { IngestionTracesServer } = await import('./servers/ingestion-traces-server.js')
            return new IngestionTracesServer()
        }

        case PluginServerMode.push_api: {
            const { PushApiServer } = await import('./servers/push-api-server.js')
            return new PushApiServer()
        }

        default: {
            // CDP modes, evaluation scheduler, local dev (null), local-cdp
            const { PluginServer } = await import('./server.js')
            return new PluginServer()
        }
    }
}

initTracing()
initMetrics()
void createServer().then((server) => server.start())
