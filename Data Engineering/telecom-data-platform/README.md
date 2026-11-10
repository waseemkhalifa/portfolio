Producer
  ↓
Kafka
  ↓
Consumer
  ↓
Bronze Storage

## Silver processing

The silver event scripts share `spark/silver/silver_event_processor.py`, which
filters rows missing `event_id` or `customer_id`, lowercases `event_type`, adds
`processed_timestamp`, and writes to `data/silver/<event_name>`.

Run an existing pipeline from this project directory:

```bash
python spark/silver/silver_customer_events.py
```

To add another event pipeline, create a small `silver_<name>_events.py` entry
point like this:

```python
from silver_event_processor import process_silver_events


if __name__ == "__main__":
    process_silver_events("network_events")
```

Pass a different `required_columns` tuple if that event has different required
fields.
