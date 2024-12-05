#!/bin/bash

set -e

# Wait for MariaDB to be ready
echo "Waiting for MariaDB to be ready..."
until mysql -h"$HIVE_METASTORE_DB_HOST" -u"$HIVE_METASTORE_DB_USER" -p"$HIVE_METASTORE_DB_PASSWORD" -e 'select 1'; do
  >&2 echo "MariaDB is unavailable - sleeping"
  sleep 5
done
echo "MariaDB is up - continuing..."

# Initialize the Hive Metastore schema if not already initialized
if [ ! -f /data/hive_metastore_initialized.flag ]; then
  echo "Initializing Hive Metastore schema..."
  schematool -initSchema -dbType mysql \
    -userName "$HIVE_METASTORE_DB_USER" \
    -passWord "$HIVE_METASTORE_DB_PASSWORD" \
    -url "jdbc:mysql://$HIVE_METASTORE_DB_HOST:$HIVE_METASTORE_DB_PORT/$HIVE_METASTORE_DB_NAME"
  touch /data/hive_metastore_initialized.flag
else
  echo "Hive Metastore schema already initialized."
fi

# Start Hive Metastore service
echo "Starting Hive Metastore service..."
hive --service metastore -p 9083
