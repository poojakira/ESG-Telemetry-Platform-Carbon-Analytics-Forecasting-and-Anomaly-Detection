"""Simple concurrency/stress tester for the FastAPI prediction endpoint.

Run a local server first (e.g. ``uvicorn app.main:app --port 8000``) then execute this
script. It will pull sample rows from the training dataset, fire a configurable
number of concurrent requests and report average latency plus error rate.  This
helps you see how many requests the API can handle before latency or failures
start to climb.

Usage example:

    python stress_test.py --concurrency 20 --requests 1000

"""

import argparse
import asyncio
import random
import time
import os
import httpx
import pandas as pd

# reuse the same feature list used during training
FEATURES = [
    "raw_material_energy", "raw_material_emission_factor", "raw_material_waste",
    "manufacturing_energy", "manufacturing_efficiency", "manufacturing_water_usage",
    "transport_distance_km", "transport_mode_factor", "logistics_energy",
    "usage_energy_consumption", "usage_duration_hours", "grid_carbon_intensity",
    "recycling_efficiency", "disposal_emission_factor", "recovered_material_value",
    "state_complexity_index", "policy_action_score", "optimization_reward_signal"
]

# default CSV path (relative to this script).  We'll also fall back
# to `backend/data` when the script is executed from the repo root.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "data/dpp_data.csv")

# fallback if the file doesn't exist (e.g. running from workspace root)
if not os.path.exists(DATA_FILE):
    alt = os.path.join(os.getcwd(), "backend", "data", "dpp_data.csv")
    if os.path.exists(alt):
        DATA_FILE = alt



def load_samples():
    """Load dataset and convert to list of dicts suitable for the API."""
    df = pd.read_csv(DATA_FILE)
    records = df[FEATURES].to_dict(orient="records")
    return records


async def worker(client: httpx.AsyncClient, uri: str, samples: list, results: list):
    """Send one request using a random sample."""
    payload = random.choice(samples)
    start = time.monotonic()
    try:
        r = await client.post(uri, json=payload, timeout=10.0)
        elapsed = time.monotonic() - start
        results.append((elapsed, r.status_code, r.text))
    except Exception as exc:
        elapsed = time.monotonic() - start
        results.append((elapsed, None, str(exc)))


async def run_test(concurrency: int, total_requests: int, uri: str):
    samples = load_samples()
    results = []
    sem = asyncio.Semaphore(concurrency)

    async def gated():
        async with sem:
            await worker(client, uri, samples, results)

    async with httpx.AsyncClient() as client:
        tasks = [gated() for _ in range(total_requests)]
        await asyncio.gather(*tasks)

    # report
    latencies = [r[0] for r in results]
    errors = [r for r in results if r[1] != 200]
    print(f"Total requests: {len(results)}")
    print(f"Successful: {len(results)-len(errors)}, Errors: {len(errors)}")
    if latencies:
        print(f"Avg latency: {sum(latencies)/len(latencies):.4f}s")
        print(f"Max latency: {max(latencies):.4f}s")
        p90 = sorted(latencies)[int(len(latencies)*0.9)]
        print(f"90th percentile: {p90:.4f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stress test the FastAPI prediction endpoint")
    parser.add_argument("--concurrency", type=int, default=10, help="Number of concurrent connections")
    parser.add_argument("--requests", type=int, default=200, help="Total number of requests to send")
    parser.add_argument("--url", type=str, default="http://127.0.0.1:8000/predict", help="Prediction endpoint URL")
    args = parser.parse_args()

    print(f"Starting test: concurrency={args.concurrency}, total_requests={args.requests}")
    asyncio.run(run_test(args.concurrency, args.requests, args.url))
