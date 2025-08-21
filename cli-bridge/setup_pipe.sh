#!/usr/bin/env bash
set -euo pipefail

# 로그 디렉토리 생성
mkdir -p logs

pane="$1"
name="$2"
outfile="logs/${name}.out"

# tmux pipe-pane으로 출력을 파일로 캡처
tmux pipe-pane -t "$pane" -o "tee $outfile >/dev/null"
echo "[pipe] $name -> $outfile"