#!/usr/bin/env bash
# 機能一覧（feature_list.json）が全部 passes になるまで、毎回新しいセッションで claude -p を回す。
#
# 使い方:
#   MAX_ITER=1 ./factory.sh           # まず 1 回だけ
#   MAX_ITER=5 MAX_STALL=2 ./factory.sh
#
# 止まる条件（ガード）:
#   完了判定  … passes: false が 0 件になった
#   回数上限  … MAX_ITER 回まわした
#   停滞検知  … 残り件数が MAX_STALL 回続けて減らなかった
#   改竄検知  … passes 以外（description や steps）が書き換えられた
#   予算上限  … 1 セッションの費用を --max-budget-usd で抑える
set -euo pipefail

MAX_ITER=${MAX_ITER:-5}
MAX_STALL=${MAX_STALL:-2}
SESSION_BUDGET=${SESSION_BUDGET:-2}

# 残り件数と、passes を除いた機能一覧のハッシュ（python3 の標準ライブラリだけで計算する）
remaining() {
  python3 -c 'import json; print(sum(not f["passes"] for f in json.load(open("feature_list.json"))))'
}
spec_hash() {
  python3 -c 'import json, hashlib
fs = [{k: v for k, v in f.items() if k != "passes"} for f in json.load(open("feature_list.json"))]
print(hashlib.sha256(json.dumps(fs, sort_keys=True).encode()).hexdigest())'
}
cost() { python3 -c 'import json, sys; print("費用: $%s" % json.load(open(sys.argv[1]))["total_cost_usd"])' "$1"; }

mkdir -p .factory
stall=0
for i in $(seq 1 "$MAX_ITER"); do
  before=$(remaining)
  if [ "$before" -eq 0 ]; then
    echo "完了: すべての機能が passes になった"
    exit 0
  fi
  hash_before=$(spec_hash)

  echo "== session $i（残り $before 件）"
  claude -p "$(cat prompts/coding.md)" \
    --permission-mode auto --permission-prompts none \
    --max-budget-usd "$SESSION_BUDGET" \
    --output-format json > ".factory/session-$i.json" || echo "session $i: claude が失敗を返した"
  cost ".factory/session-$i.json" || true

  if [ "$(spec_hash)" != "$hash_before" ]; then
    echo "停止: feature_list.json の passes 以外が書き換えられた（git diff で確かめる）"
    exit 1
  fi

  after=$(remaining)
  if [ "$after" -lt "$before" ]; then stall=0; else stall=$((stall + 1)); fi
  if [ "$stall" -ge "$MAX_STALL" ]; then
    echo "停止: $MAX_STALL 回続けて残り件数が減らなかった"
    exit 1
  fi
done
echo "停止: MAX_ITER（$MAX_ITER 回）に達した。残り $(remaining) 件"
