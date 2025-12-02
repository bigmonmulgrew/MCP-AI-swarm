import requests
import concurrent.futures
import time

API_URL = "http://127.0.0.1:9090/query"

def send_query(prompt: str, idx: int):
    payload = {
        "prompt": prompt,
        "model": "phi4",
        "options": {}
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=120)
        response.raise_for_status()
        return idx, response.json()
    except Exception as e:
        return idx, {"error": str(e)}

def main():
    print("=== AI Queue Concurrent Test ===")

    # test queries (can be the same or different)
    prompts = [
        "Write a short joke.",
        "Give me a small maths challenge for a child.",
        "Describe a cat in one sentence.",
        "Explain gravity in one sentence.",
        "What is 2+2?",
        "Tell me a random fun fact.",
    ]

    start = time.time()

    # Fire ALL requests concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(prompts)) as executor:
        futures = [
            executor.submit(send_query, prompt, i)
            for i, prompt in enumerate(prompts)
        ]

        # Print results as they complete
        for future in concurrent.futures.as_completed(futures):
            idx, result = future.result()
            print(f"\n=== Result #{idx} ===")
            print(result)

    end = time.time()
    print(f"\n=== Test Complete in {end - start:.2f} seconds ===")


if __name__ == "__main__":
    main()
