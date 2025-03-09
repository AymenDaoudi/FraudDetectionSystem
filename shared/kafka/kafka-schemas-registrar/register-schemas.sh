#!/bin/sh

echo "Starting registering schemas..."

SCHEMA_REGISTRY_URL="schema-registry"
SUBJECT="Payment-value"
# Define the Avro schema for the Payment record
AVRO_SCHEMA='{"schema": "{\"type\": \"record\", \"name\": \"Payment\", \"fields\": [{\"name\": \"operation_id\", \"type\": {\"type\": \"string\", \"logicalType\": \"uuid\"}}, {\"name\": \"user_id\", \"type\": {\"type\": \"string\", \"logicalType\": \"uuid\"}}, {\"name\": \"date\", \"type\": {\"type\": \"long\", \"logicalType\": \"timestamp-millis\"}}, {\"name\": \"price\", \"type\": {\"type\": \"bytes\", \"logicalType\": \"decimal\", \"precision\": 10, \"scale\": 2}}]}"}'

# Register the schema using Schema Registry's REST API.
curl -X POST "http://${SCHEMA_REGISTRY_URL}:8081/subjects/${SUBJECT}/versions" \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data "$AVRO_SCHEMA"

echo "Verifying if the schema was registered successfully..."

echo "Checking if subject '${SUBJECT}' exists in the Schema Registry..."

# Retrieve all subjects
SUBJECTS=$(curl -s -X GET "http://${SCHEMA_REGISTRY_URL}:8081/subjects")

# Check if the subject is present in the list
if echo "${SUBJECTS}" | grep -q "\"${SUBJECT}\""; then
    echo "Subject '${SUBJECT}' found."
    
    # Retrieve and display all registered versions for the subject
    echo "Fetching registered versions for '${SUBJECT}'..."
    VERSIONS=$(curl -s -X GET "${SCHEMA_REGISTRY_URL}/subjects/${SUBJECT}/versions")
    echo "Versions: ${VERSIONS}"
    
    # Retrieve and display the latest schema definition for the subject
    echo "Fetching the latest schema for '${SUBJECT}'..."
    LATEST_SCHEMA=$(curl -s -X GET "${SCHEMA_REGISTRY_URL}/subjects/${SUBJECT}/versions/latest")
    echo "Latest Schema:"
    echo "${LATEST_SCHEMA}" | jq .

    echo "Schemas registered successfully."
else
    echo "Subject '${SUBJECT}' not found in the Schema Registry."
fi

# Keep the container running
tail -f /dev/null