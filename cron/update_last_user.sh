#!/bin/bash

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting script..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
ENV_FILE="$SCRIPT_DIR/../.env"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Using .env file: $ENV_FILE"

if [ -f "$ENV_FILE" ]; then
	    export $(grep -v '^#' "$ENV_FILE" | xargs)
	        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Environment variables loaded."
	else
		    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: .env not found at $ENV_FILE"
		        exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running MySQL query..."

mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -D "$DB_NAME" << 'SQL'
INSERT INTO last_user (hardware_id, user_id)
SELECT ID, USERID FROM hardware
WHERE USERID IS NOT NULL AND USERID <> ''
ON DUPLICATE KEY UPDATE
    user_id = VALUES(user_id),
    last_update = CURRENT_TIMESTAMP;
SQL

if [ $? -eq 0 ]; then
	    echo "[$(date '+%Y-%m-%d %H:%M:%S')] MySQL query executed successfully."
    else
	        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: MySQL query failed."
		    exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Script finished."

