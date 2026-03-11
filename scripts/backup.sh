#!/bin/bash
# LITHO-SONIC backup script

BACKUP_DIR="/data/lithosonic/backup"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="lithosonic_backup_${DATE}.tar.gz"

echo "Starting backup: $DATE"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
if [ -f "data/lithosonic.db" ]; then
    cp data/lithosonic.db $BACKUP_DIR/lithosonic_${DATE}.db
    echo "✅ Database backed up"
fi

# Backup configuration
tar -czf $BACKUP_DIR/config_${DATE}.tar.gz config/ 2>/dev/null
echo "✅ Configuration backed up"

# Backup processed data
if [ -d "data/processed" ]; then
    tar -czf $BACKUP_DIR/processed_${DATE}.tar.gz data/processed/ 2>/dev/null
    echo "✅ Processed data backed up"
fi

# Create archive
tar -czf $BACKUP_DIR/$BACKUP_FILE \
    $BACKUP_DIR/lithosonic_${DATE}.db \
    $BACKUP_DIR/config_${DATE}.tar.gz \
    $BACKUP_DIR/processed_${DATE}.tar.gz 2>/dev/null

# Clean up temporary files
rm $BACKUP_DIR/lithosonic_${DATE}.db
rm $BACKUP_DIR/config_${DATE}.tar.gz
rm $BACKUP_DIR/processed_${DATE}.tar.gz

echo "✅ Backup complete: $BACKUP_DIR/$BACKUP_FILE"
