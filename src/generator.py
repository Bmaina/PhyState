import numpy as np

class EvidenceGenerator:
    """Simulates multi-sensor physical evidence streams across 5 agricultural scenarios."""

    def __init__(self, seed: int = 42):
        np.random.seed(seed)

    def generate_scenario_data(self, n_samples_per_scenario: int = 50):
        data = []
        labels = []
        scenarios = [
            "SUPPORTED_NORMAL_CROP",
            "CONFLICTED_CROP_FAILURE",
            "CONFLICTED_UNPLANTED_LAND",
            "UNDERDETERMINED_HIGH_CLOUD",
            "UNDERDETERMINED_SENSOR_LATENCY"
        ]

        for scenario_idx, scenario in enumerate(scenarios):
            for _ in range(n_samples_per_scenario):
                if scenario == "SUPPORTED_NORMAL_CROP":
                    # High NDVI, high SAR canopy response, normal rainfall
                    ndvi_mean = np.random.normal(0.75, 0.04)
                    sar_vv_vh = np.random.normal(-10.0, 0.8)
                    rain_anomaly = np.random.normal(1.0, 0.1)
                    cloud_cover = np.random.uniform(0.0, 0.2)
                    data_age_days = np.random.uniform(1, 3)
                    true_label = "SUPPORTED"

                elif scenario == "CONFLICTED_CROP_FAILURE":
                    # Low NDVI, low SAR, severely low rainfall (Claim: Normal Crop)
                    ndvi_mean = np.random.normal(0.25, 0.05)
                    sar_vv_vh = np.random.normal(-18.0, 1.0)
                    rain_anomaly = np.random.normal(0.2, 0.1)
                    cloud_cover = np.random.uniform(0.0, 0.2)
                    data_age_days = np.random.uniform(1, 3)
                    true_label = "CONFLICTED"

                elif scenario == "CONFLICTED_UNPLANTED_LAND":
                    # Bare soil signature despite active crop growth claim
                    ndvi_mean = np.random.normal(0.15, 0.03)
                    sar_vv_vh = np.random.normal(-22.0, 1.2)
                    rain_anomaly = np.random.normal(0.9, 0.1)
                    cloud_cover = np.random.uniform(0.0, 0.15)
                    data_age_days = np.random.uniform(1, 3)
                    true_label = "CONFLICTED"

                elif scenario == "UNDERDETERMINED_HIGH_CLOUD":
                    # High optical obstruction, noisy signals
                    ndvi_mean = np.random.normal(0.45, 0.20)
                    sar_vv_vh = np.random.normal(-12.0, 2.5)
                    rain_anomaly = np.random.normal(1.0, 0.2)
                    cloud_cover = np.random.uniform(0.85, 0.99)  # Obstruction
                    data_age_days = np.random.uniform(1, 5)
                    true_label = "UNDERDETERMINED"

                elif scenario == "UNDERDETERMINED_SENSOR_LATENCY":
                    # Stale evidence streams beyond validity threshold
                    ndvi_mean = np.random.normal(0.70, 0.05)
                    sar_vv_vh = np.random.normal(-11.0, 1.0)
                    rain_anomaly = np.random.normal(1.0, 0.1)
                    cloud_cover = np.random.uniform(0.1, 0.3)
                    data_age_days = np.random.uniform(25, 45)  # Stale data (>20 days)
                    true_label = "UNDERDETERMINED"

                sample = {
                    "scenario_name": scenario,
                    "ndvi_mean": max(0.0, min(1.0, ndvi_mean)),
                    "sar_vv_vh": sar_vv_vh,
                    "rain_anomaly": rain_anomaly,
                    "cloud_cover": cloud_cover,
                    "data_age_days": data_age_days,
                    "true_label": true_label
                }
                data.append(sample)
                labels.append(true_label)

        return data, labels
   