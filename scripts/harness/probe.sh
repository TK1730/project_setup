#!/usr/bin/env bash
# 同じ確認用の依頼を、変更前と変更後のハーネスで実行して結果を並べて保存する。
#
# 使い方:
#   scripts/harness/probe.sh <変更前の git ref> <依頼文のファイル>
#   DRY_RUN=1 scripts/harness/probe.sh HEAD probe.txt   # claude を呼ばずに流れだけ確かめる
#
# 変更前は <ref> の時点の別の作業フォルダ（git worktree）で、変更後は今の作業フォルダで実行する。
# どちらも読み取り専用で動かし、ファイルを書き換えさせない。
set -euo pipefail

if [ $# -ne 2 ]; then
  echo "使い方: $0 <変更前の git ref> <依頼文のファイル>" >&2
  exit 2
fi
before_ref=$1
prompt_file=$(realpath "$2")
repo_root=$(git rev-parse --show-toplevel)
out_dir="$repo_root/.local/harness/probe-results/$(date +%Y%m%d-%H%M%S)-$(basename "$prompt_file" .txt)"
worktree=$(mktemp -d)

cleanup() { git -C "$repo_root" worktree remove --force "$worktree" >/dev/null 2>&1 || true; }
trap cleanup EXIT

run_probe() { # $1: 実行する作業フォルダ, $2: 結果のファイル
  if [ "${DRY_RUN:-}" = 1 ]; then
    echo "[dry-run] $1 で依頼を実行 -> $2"
    return
  fi
  (cd "$1" && claude -p "$(cat "$prompt_file")" \
    --permission-mode plan \
    --permission-prompts none \
    --disallowed-tools "Edit Write NotebookEdit Bash" \
    --no-session-persistence \
    --max-budget-usd 1) >"$2"
}

mkdir -p "$out_dir"
cp "$prompt_file" "$out_dir/prompt.txt"
git -C "$repo_root" worktree add --detach "$worktree" "$before_ref" >/dev/null 2>&1

run_probe "$worktree" "$out_dir/before.md"
run_probe "$repo_root" "$out_dir/after.md"

echo "結果: $out_dir"
echo "比べる: diff $out_dir/before.md $out_dir/after.md"
