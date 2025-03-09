#!/bin/bash
# Start the Schema Registry process in the background
/etc/confluent/docker/run &
registry_pid=$!

echo "Waiting for the Schema Registry to start..."
# Wait until the Schema Registry is available (adjust the URL and sleep interval as needed)
until curl -s http://localhost:8081/subjects > /dev/null; do
  sleep 3
done

echo "Schema Registry is up. Registering schema..."

/etc/confluent/docker/register_schemas.sh

# Wait on the Schema Registry process to keep the container running
wait $registry_pid