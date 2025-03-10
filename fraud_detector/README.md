# Fraud Detector

A Kafka Streams application that consumes payment messages in Avro format from a Kafka topic and processes them for fraud detection.

## Prerequisites

- Java 11 or higher
- Maven
- Apache Kafka
- Confluent Schema Registry

## Building the Application

To build the application, run:

```bash
mvn clean package
```

This will create an executable JAR file with all dependencies included.

## Configuration

The application can be configured by modifying the `src/main/resources/application.properties` file:

```properties
# Kafka Configuration
bootstrap.servers=localhost:9092
schema.registry.url=http://localhost:8081
application.id=fraud-detector-app

# Topic Configuration
payment.topic=payments

# Streams Configuration
commit.interval.ms=1000
cache.max.bytes.buffering=10485760
auto.offset.reset=earliest
```

## Running the Application

To run the application, use:

```bash
java -jar target/fraud-detector-1.0-SNAPSHOT-jar-with-dependencies.jar
```

## Implementing Fraud Detection Logic

The fraud detection logic can be implemented in the `buildTopology` method of the `FraudDetectorApp` class. The current implementation includes a placeholder where you can add your custom fraud detection logic:

```java
// TODO: Add fraud detection logic here
// This is where you'll implement your fraud detection logic later
```

## Avro Schema

The application uses the following Avro schema for payment messages:

```json
{
  "namespace": "frauddetection.payment.avro",
  "type": "record",
  "name": "Payment",
  "fields": [
    {
      "name": "transaction_id",
      "type": {
        "type": "string",
        "logicalType": "uuid"
      }
    },
    {
      "name": "user_id",
      "type": {
        "type": "string",
        "logicalType": "uuid"
      }
    },
    {
      "name": "date",
      "type": {
        "type": "long",
        "logicalType": "timestamp-millis"
      }
    },
    {
      "name": "nb_of_items",
      "type": "int"
    },
    {
      "name": "total_amount",
      "type": {
        "type": "bytes",
        "logicalType": "decimal",
        "precision": 10,
        "scale": 2
      }
    }
  ]
}
``` 