#!/usr/bin/env bash
# Runs ~/queue/*.job in name order, one at a time; new jobs can be dropped in while it runs. Stops when the queue is
# empty and ~/queue/STOP exists. Output: ~/logs/queue.log.   usage: nohup bash queue.sh > ~/logs/queue.log 2>&1 &
mkdir -p ~/queue ~/queue/done ~/logs
while true; do
  j=$(ls ~/queue/*.job 2>/dev/null | head -1)
  if [ -z "$j" ]; then [ -f ~/queue/STOP ] && { echo "QUEUE EMPTY $(date +%T)"; break; }; sleep 20; continue; fi
  n=$(basename "$j"); mv "$j" ~/queue/done/"$n"
  echo "##### JOB $n $(date +%T)"
  bash ~/queue/done/"$n"
  echo "##### END $n $(date +%T)"
done
