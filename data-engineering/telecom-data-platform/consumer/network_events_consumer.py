from event_consumer import run_consumer


if __name__ == "__main__":
    run_consumer("network-events", "data/network_events.jsonl")
