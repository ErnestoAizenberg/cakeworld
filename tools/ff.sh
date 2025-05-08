#!/bin/bash
if [ -z "$1" ]; then
  echo "Использование: $0 имя_файла"
  exit 1
fi
filename="$1"
find . -type f -name "$filename" -printf '%P\n'
