#!/usr/bin/env bash
declare -A TMUX_PANES

register_pane() {
  local name="$1"
  local target="$2"   # session:window.pane
  TMUX_PANES["$name"]="$target"
  echo "[bridge] registered $name -> $target"
}

send_to() {
  local name="$1"
  shift
  local text="$*"
  local target="${TMUX_PANES[$name]}"
  if [ -z "$target" ]; then
    echo "[bridge] unknown target: $name" >&2
    return 1
  fi
  tmux send-keys -t "$target" "$text" Enter
  echo "[bridge] sent to $name ($target): $text"
}

list_panes() {
  for k in "${!TMUX_PANES[@]}"; do
    echo "$k -> ${TMUX_PANES[$k]}"
  done
}