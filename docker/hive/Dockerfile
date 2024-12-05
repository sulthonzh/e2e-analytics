# Use an openjdk base image suitable for ARM64
FROM openjdk:8-jdk-slim

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends wget gnupg curl tar bash default-mysql-client

# Download Apache Hadoop binaries
RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz \
    && tar -xzvf hadoop-3.3.1.tar.gz \
    && mv hadoop-3.3.1 /opt/hadoop \
    && rm hadoop-3.3.1.tar.gz

# Download Apache Hive binaries (updated to use a different version)
RUN wget https://archive.apache.org/dist/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz \
    && tar -xzvf apache-hive-3.1.3-bin.tar.gz \
    && mv apache-hive-3.1.3-bin /opt/hive \
    && rm apache-hive-3.1.3-bin.tar.gz

# Install MySQL JDBC connector
RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.29.tar.gz \
    && tar -xzvf mysql-connector-java-8.0.29.tar.gz \
    && mv mysql-connector-java-8.0.29/mysql-connector-java-8.0.29.jar /opt/hive/lib/ \
    && rm -rf mysql-connector-java-8.0.29*

# Set environment variables for Hive and Hadoop
ENV HIVE_HOME=/opt/hive
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_PREFIX=/opt/hadoop
ENV PATH=$PATH:$HIVE_HOME/bin:$HADOOP_HOME/bin

# Copy entrypoint script
COPY docker/hive/entrypoint.sh /opt/entrypoint.sh

# Set permissions and make the script executable
RUN chmod +x /opt/entrypoint.sh

# Set entrypoint to the script
ENTRYPOINT ["/opt/entrypoint.sh"]
