#!/bin/bash
#xargs -n 1 curl -C - -k -O < urls.txt
set -e
while read line; do
  echo $line
  FI=$(echo $line | cut -d / -f 5)
  if [[ ! -f $FI ]]; then
    if [[ -f ${FI}_uploaded_.jpg ]]; then
      echo "  but uploaded - no download"
    else
      echo " download"
      curl -k -O $line
    fi
  fi
#done < urls-head.txt
done < urls.txt
