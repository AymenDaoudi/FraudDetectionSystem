package com.frauddetection;

import frauddetection.payment.avro.Payment;
import io.confluent.kafka.streams.serdes.avro.SpecificAvroSerde;
import io.confluent.kafka.serializers.AbstractKafkaSchemaSerDeConfig;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.KStream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.math.BigDecimal;
import java.util.Properties;
import org.apache.avro.Conversions;
import org.apache.avro.LogicalTypes;
import org.apache.avro.Schema;

public class FraudDetectorApp {
    
    private static Logger LOG = LoggerFactory.getLogger(FraudDetectorApp.class);

    public static void main(String[] args) {

        LOG.info("Reading configuration...");

        Properties props = new Properties();

        // Disable JMX metrics to avoid NullPointerException in containerized environment
        props.put(StreamsConfig.METRICS_RECORDING_LEVEL_CONFIG, "INFO");

        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "fraud-detection-application");

        // Use environment variables if available, otherwise use defaults from application.properties
        String bootstrapServers = System.getenv("KAFKA_BOOTSTRAP_SERVERS");
        if (bootstrapServers == null || bootstrapServers.isEmpty()) {
            bootstrapServers = "localhost:9092";
        }

        LOG.info("Bootstrap servers: {}", bootstrapServers);

        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);

        String schemaRegistryUrl = System.getenv("SCHEMA_REGISTRY_URL");
        if (schemaRegistryUrl == null || schemaRegistryUrl.isEmpty()) {
            schemaRegistryUrl = "http://localhost:8081";
        }

        LOG.info("Schema registry URL: {}", schemaRegistryUrl);

        props.put(AbstractKafkaSchemaSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG, schemaRegistryUrl);

        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, SpecificAvroSerde.class);

        StreamsBuilder streamsBuilder = new StreamsBuilder();

        KStream<String, Payment> stream = streamsBuilder.stream("payments");

        stream
            .peek(FraudDetectorApp::printOnEnter)
            .filter((transactionId, payment) -> 
                payment.getUserId().toString().equals("NONE") || 
                payment.getNbOfItems() > 1000 || 
                payment.getTotalAmount().compareTo(BigDecimal.valueOf(10000)) > 0
            )
            .peek(FraudDetectorApp::printOnExit)
            .to("fraudulent-payments");

        Topology topology = streamsBuilder.build();

        KafkaStreams streams = new KafkaStreams(topology, props);

        LOG.info("Starting streams...");
        streams.start();

        LOG.info("Streams started");

        
        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));

        LOG.info("Streams closed");
    }

    private static void printOnEnter(String transactionId, Payment payment) {
        LOG.info("\n*******************************************");
        LOG.info("ENTERING stream transaction with ID < " + transactionId + " >, " +
                "of user < " + payment.getUserId() + " >, total amount < " + payment.getTotalAmount() +
                " > and nb of items < " + payment.getNbOfItems() + " >");
    }

    private static void printOnExit(String transactionId, Payment payment) {
        LOG.info("EXITING from stream transaction with ID < " + transactionId + " >, " +
                "of user < " + payment.getUserId() + " >, total amount < " + payment.getTotalAmount() +
                " > and number of items < " + payment.getNbOfItems() + " >");
    }
} 