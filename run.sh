#!/bin/bash

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SOURCE_DIR"

LOG=$(date +%s)".log"

./record_data.py > "$LOG"

if [ ! -s "$LOG" ]
then
	rm "$LOG"
fi
