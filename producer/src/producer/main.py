import time

import numpy as np
import orjson
import pandas as pd
from kafka import KafkaProducer

# Kafka konfigurace
BROKER_URL = "redpanda:9092"
TOPIC = "test_topic"


# Definice funkce pro serializaci
def orjson_serializer(data):
    # Ensure all dictionary keys are strings
    if isinstance(data, dict):
        data = {str(k): v for k, v in data.items()}
    return orjson.dumps(data)


# Vytvořte Kafka producenta
producer = KafkaProducer(
    bootstrap_servers=BROKER_URL,
    value_serializer=orjson_serializer,  # Use custom orjson serializer
    key_serializer=lambda k: k.encode("utf-8"),  # Serialize key to bytes
)

num_records = 20000

# Generování časových razítek
start_date = "2009-08-18 23:00:00"
timestamps = pd.date_range(start=start_date, periods=num_records, freq="s")
prices = np.random.uniform(low=50.0, high=100.0, size=num_records)

# Vytvoření pandas.Series a převod na dictionary
df = pd.Series(data=prices, index=timestamps, name="price")
data = df.to_dict()  # Convert Series to dictionary with string keys

# Nastavení dummy klíče
dummy_key = "dummy_key"

# Měření času
start_time = time.time()

# Odeslání celé zprávy do Kafka
metadata = producer.send(TOPIC, key=dummy_key, value=data).get(timeout=10)
producer.flush()

print(f"Message sent to partition {metadata.partition} with offset {metadata.offset}")

end_time = time.time()

print(f"Message sent in {end_time - start_time:.4f} seconds")
