from dagster_k8s import k8s_job_executor

job_ttl = {
    "dagster-k8s/config": {
        "job_spec_config": {"ttl_seconds_after_finished": 60}  # Set TTL to 1 minute
    }
}

job_executor = k8s_job_executor.configured(
    {
        "step_k8s_config": {
            "container_config": {
                "resources": {
                    "requests": {
                        "cpu": "2",
                        "memory": "2Gi"
                    },
                }
            }
        },
        "max_concurrent": 20,
    }
)
