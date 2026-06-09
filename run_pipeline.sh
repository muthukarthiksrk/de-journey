#!/bin/bash

PIPELINE_DIR="$HOME/clouddrive/de-journey"
LOG_FILE="$PIPELINE_DIR/pipeline.log"
PYTHON="/usr/bin/python3"
SCRIPT="$PIPELINE_DIR/day02.py"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "==============================="
log "Pipeline run started"
log "==============================="

log "Running weather pipeline..."
$PYTHON "$SCRIPT" >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log "Pipeline completed successfully"
else
    log "ERROR: Pipeline failed"
fi

log "==============================="
