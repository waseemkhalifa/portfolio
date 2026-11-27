from event_consumer import run_consumer


if __name__ == "__main__":
    run_consumer("billing-events", "data/billing_events.jsonl")
