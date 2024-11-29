#!/usr/bin/sh

runpod create pods \
  --name nl-conflict-llm \
  --gpuType "NVIDIA A40" \
  --imageName "runpod/pytorch:3.10-2.0.0-117" \
  --containerDiskSize 10 \
  --volumeSize 100 \
  --args "bash -c 'mkdir /testdir1 && ./start.sh'"
