FROM maven:3.8-openjdk-11 AS build

# Set working directory
WORKDIR /app

# Copy the pom.xml file
COPY ./pom.xml .

# Copy the source code
COPY ./src ./src

# Build the application with the maven-jar-plugin and maven-shade-plugin configured
RUN mvn clean package -DskipTests

# Create a lightweight JRE image
FROM openjdk:11-jre-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV KAFKA_BOOTSTRAP_SERVERS=kafka:29092
ENV SCHEMA_REGISTRY_URL=http://schema-registry:8081

# Copy the built JAR file from the build stage
COPY --from=build /app/target/fraud-detector-1.0-SNAPSHOT.jar /app/fraud-detector.jar

# Copy the configuration files
COPY ./src/main/resources/log4j.properties /app/log4j.properties

# Set the entrypoint to run the JAR with the properly configured manifest
CMD ["java", "-jar", "fraud-detector.jar"]