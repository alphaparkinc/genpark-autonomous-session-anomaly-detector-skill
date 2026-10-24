from client import AutonomousSessionAnomalyDetectorClient
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    detector = AutonomousSessionAnomalyDetectorClient()
    print("=== AUTONOMOUS SESSION ANOMALY DETECTOR ===")
    
    # 1. Normal user session
    normal_session = {"session_id": "sess_norm_01", "clicks_per_minute": 16.0, "keystroke_interval_ms": 135.0, "geo_hop_speed_kmh": 0.0, "api_endpoint_entropy": 2.1}
    res_normal = detector.detect_session_anomalies(normal_session)
    print(f"1. Normal Session: Risk={res_normal['risk_score']}/100 | Class={res_normal['classification']}")
    print(f"   Action: {res_normal['recommended_action']}")

    # 2. Automated credential-stuffing bot / impossible travel hop
    anomalous_session = {"session_id": "sess_bot_99", "clicks_per_minute": 180.0, "keystroke_interval_ms": 8.0, "geo_hop_speed_kmh": 1250.0, "api_endpoint_entropy": 0.3}
    res_anom = detector.detect_session_anomalies(anomalous_session)
    print()
    print(f"2. Bot/Takeover Session: Risk={res_anom['risk_score']}/100 | Class={res_anom['classification']}")
    print(f"   Action: {res_anom['recommended_action']}")
    print("   Flagged Deviations:")
    for d in res_anom['flagged_deviations']:
        print(f"     - {d['feature']}: {d['observed_value']} (Z-score: {d['z_score']}) [{d['deviation_level']}]")

if __name__ == "__main__":
    main()
