#!/bin/bash
# LITHO-SONIC restore script

if [ -z "$1" ]; then
    echo "Usage: $0 <backup-file.tar.gz>"
    exit 1
fi

BACKUP_FILE=$1
RESTORE_DIR="/tmp/lithosonic_restore"

echo "Restoring from: $BACKUP_FILE"

# Create restore directory
mkdir -p $RESTORE_DIR

# Extract backup
tar -xzf $BACKUP_FILE -C $RESTORE_DIR

# Restore database
if [ -f "$RESTORE_DIR/lithosonic_*.db" ]; then
    cp $RESTORE_DIR/lithosonic_*.db data/lithosonic.db
    echo "✅ Database restored"
fi

# Restore configuration
if [ -f "$RESTORE_DIR/config_*.tar.gz" ]; then
    tar -xzf $RESTORE_DIR/config_*.tar.gz -C .
    echo "✅ Configuration restored"
fi

# Restore processed data
if [ -f "$RESTORE_DIR/processed_*.tar.gz" ]; then
    tar -xzf $RESTORE_DIR/processed_*.tar.gz -C .
    echo "✅ Processed data restored"
fi

# Clean up
rm -rf $RESTORE_DIR

echo "✅ Restore complete"
