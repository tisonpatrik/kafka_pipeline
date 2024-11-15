import time

import orjson
from kafka import KafkaConsumer

# Kafka konfigurace
BROKER_URL = "redpanda:9092"
TOPIC = "test_topic"


# Definice funkce pro deserializaci
def orjson_deserializer(data):
    # Deserialize JSON bytes back to Python objects
    return orjson.loads(data)


# Vytvoření Kafka konzumenta
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BROKER_URL,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my-group",  # Nastavení skupiny pro konzumenta
    value_deserializer=orjson_deserializer,  # Použití vlastní deserializace
)

# Příjem zpráv a logování časů
for message in consumer:
    start_time = time.time()
    print(
        f"Started receiving message at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}"
    )

    # Zpracování zprávy
    value = message.value  # Získání deserializované hodnoty
    print("Received message (type):", type(value))
    print("Received message (content):", value)

    end_time = time.time()
    print(
        f"Finished receiving message at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}"
    )
    print(f"Time taken to process message: {end_time - start_time:.4f} seconds")
