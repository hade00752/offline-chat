#!/bin/bash
mkdir -p logs

echo "[*] Starting 3 mesh nodes..."

# Node A
python3 -u -m daemon.main --config config/nodeA.yaml > logs/nodeA.log 2>&1 &
PID_A=$!

# Node B
python3 -u -m daemon.main --config config/nodeB.yaml > logs/nodeB.log 2>&1 &
PID_B=$!

# Node C
python3 -u -m daemon.main --config config/nodeC.yaml > logs/nodeC.log 2>&1 &
PID_C=$!

echo "Nodes started: A=$PID_A, B=$PID_B, C=$PID_C"
echo "Logs are in logs/"

# Keep the script alive and stream logs
sleep 2
tail -f logs/nodeA.log logs/nodeB.log logs/nodeC.log
