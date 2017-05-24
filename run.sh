#!/bin/bash

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SOURCE_DIR"

LOG=$(date +%s)".log"

./record_data.py > "$LOG" 2>&1

if [ ! -s "$LOG" ]
then
	rm "$LOG"
fi
