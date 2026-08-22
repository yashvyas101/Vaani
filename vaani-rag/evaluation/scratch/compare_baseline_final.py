
import json
from pathlib import Path

BASE = Path("c:/Users/HP/OneDrive/Desktop/Vaani/vaani-rag/evaluation/results/stage3_baseline_results.jsonl")
FINAL = Path("c:/Users/HP/OneDrive/Desktop/Vaani/vaani-rag/evaluation/results/stage3_final_results.jsonl")

def compare():
    def get_stats(path):
        succ, fail, r_err = 0, 0, 0
        r_lat, g_lat, t_lat = [], [], []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                d = json.loads(line)
                if d["success"]:
                    succ += 1
                else:
                    fail += 1
                    err = d.get("error", "") or ""
                    if "429" in err:
                        r_err += 1
                t = d.get("telemetry", {})
                r_lat.append(t.get("retrieval_ms", 0.0))
                g_lat.append(t.get("gemini_generation_ms", 0.0))
                t_lat.append(t.get("total_ms", 0.0))
        return succ, fail, r_err, sum(r_lat)/len(r_lat), sum(g_lat)/len(g_lat), sum(t_lat)/len(t_lat)

    b_succ, b_fail, b_429, b_ret, b_gem, b_tot = get_stats(BASE)
    f_succ, f_fail, f_429, f_ret, f_gem, f_tot = get_stats(FINAL)

    print("Baseline (Phase 1B) Stats:")
    print(f"  Success: {b_succ}, Fail: {b_fail} (Rate Limit 429: {b_429})")
    print(f"  Avg Retrieval Latency: {b_ret:.2f} ms")
    print(f"  Avg Gemini Latency: {b_gem:.2f} ms")
    print(f"  Avg Total Latency: {b_tot:.2f} ms")

    print("\nFinal (Phase 1D) Stats:")
    print(f"  Success: {f_succ}, Fail: {f_fail} (Rate Limit 429: {f_429})")
    print(f"  Avg Retrieval Latency: {f_ret:.2f} ms")
    print(f"  Avg Gemini Latency: {f_gem:.2f} ms")
    print(f"  Avg Total Latency: {f_tot:.2f} ms")

if __name__ == "__main__":
    compare()
