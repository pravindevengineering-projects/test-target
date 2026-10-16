#!/usr/bin/env bash
# Deploy script for the order service

SERVICE_NAME=$1
DEPLOY_ENV=$2
CONFIG_DIR=/etc/orderservice

echo "Deploying $SERVICE_NAME to $DEPLOY_ENV"

# Vulnerability: unquoted variables — word splitting if SERVICE_NAME has spaces
if [ -d "$CONFIG_DIR/$SERVICE_NAME" ]; then
    echo "Config found"
fi

# Bug: pipefail not set — if tar fails, the pipe continues silently
tar -czf - ./app | ssh deployer@prod "cat > /tmp/deploy.tar.gz"

# Vulnerability: command injection via unquoted env variable in eval
eval "start_service_$DEPLOY_ENV"

# Bug: exit code of previous command not checked before critical step
rm -rf /tmp/deploy.tar.gz
echo "Cleanup done"

# Bug: using $? after a command that isn't the one we want to check
cp ./config.yml $CONFIG_DIR/$SERVICE_NAME/
STATUS=$?
echo "Removing old logs..."
rm -f /var/log/$SERVICE_NAME/*.log
# Bug: $STATUS here reflects the rm above, not the cp
if [ $STATUS -ne 0 ]; then
    echo "Config copy failed"
    exit 1
fi

echo "Deploy complete"
