#!/usr/bin/env bash
set -euo pipefail
now=${KEEPALIVE_TEST_NOW:-$(date +%s)}
last=${KEEPALIVE_TEST_LAST:-$(git log -1 --format=%ct)}
if (( now - last < 30 * 86400 )); then
  decision=skip
else
  decision=commit
fi
if [[ -n ${KEEPALIVE_TEST_NOW:-} ]]; then
  echo "$decision"
  exit 0
fi
if [[ $decision == skip ]]; then
  echo "Recent repository commit found; no keepalive needed."
  exit 0
fi
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
mkdir -p .github
date -u +'%Y-%m-%dT%H:%M:%SZ' > .github/keepalive.txt
git add .github/keepalive.txt
git commit -m 'chore: keep scheduled workflows active'
git push origin HEAD:main
