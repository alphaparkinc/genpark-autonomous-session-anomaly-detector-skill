import math, sys
sys.stdout.reconfigure(encoding='utf-8')

class AutonomousSessionAnomalyDetectorClient:
    """
    Session security analyzer computing normalized feature Z-scores and Euclidean distance
    across multidimensional behavioral signals (clicks/sec, typing intervals, geographic hop speed, API entropy).
    """
    def __init__(self):
        # Baseline normal human distributions: (mean, std)
        self.baselines = {
            "clicks_per_minute": (14.0, 6.0),
            "keystroke_interval_ms": (140.0, 35.0),
            "geo_hop_speed_kmh": (15.0, 25.0),
            "api_endpoint_entropy": (2.2, 0.4)
        }

    def compute_z_score(self, val, mean, std):
        return (val - mean) / max(1e-4, std)

    def detect_session_anomalies(self, session_telemetry):
        z_scores = {}
        deviations = []
        anomaly_weight = 0.0

        for feature, (mean, std) in self.baselines.items():
            val = session_telemetry.get(feature, mean)
            z = self.compute_z_score(val, mean, std)
            z_scores[feature] = round(z, 2)
            
            # Absolute z > 2.5 signifies statistically significant deviation (>99% confidence)
            if abs(z) >= 2.5:
                severity = "CRITICAL" if abs(z) >= 4.0 else "WARNING"
                deviations.append({
                    "feature": feature,
                    "observed_value": val,
                    "baseline_mean": mean,
                    "z_score": round(z, 2),
                    "deviation_level": severity
                })
                anomaly_weight += abs(z) * (1.5 if feature == "geo_hop_speed_kmh" else 1.0)

        # Composite risk score (0 - 100)
        risk_score = min(100.0, (anomaly_weight / 12.0) * 100.0)

        if risk_score >= 70.0:
            classification = "HIGH_RISK_SUSPECTED_TAKEOVER"
            recommended_action = "REQUIRE_IMMEDIATE_STEP_UP_MFA"
        elif risk_score >= 35.0:
            classification = "ANOMALOUS_VELOCITY_ACTIVITY"
            recommended_action = "RATE_LIMIT_SENSITIVE_ACTIONS"
        else:
            classification = "BENIGN_NORMAL_SESSION"
            recommended_action = "ALLOW_EXECUTION"

        return {
            "status": "success",
            "session_id": session_telemetry.get("session_id", "sess_unknown"),
            "risk_score": round(risk_score, 1),
            "classification": classification,
            "recommended_action": recommended_action,
            "feature_z_scores": z_scores,
            "flagged_deviations": deviations
        }
