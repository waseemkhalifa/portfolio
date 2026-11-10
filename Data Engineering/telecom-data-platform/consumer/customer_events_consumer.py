from event_consumer import run_consumer


if __name__ == "__main__":
    run_consumer("customer-events", "data/customer_events.jsonl")
