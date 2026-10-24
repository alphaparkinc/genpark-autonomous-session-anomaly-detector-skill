import sys, json
from client import AutonomousSessionAnomalyDetectorClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    detector = AutonomousSessionAnomalyDetectorClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-autonomous-session-anomaly-detector-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    res = detector.detect_session_anomalies(req)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
