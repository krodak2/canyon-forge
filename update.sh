#!/bin/bash
# Canyon Forge — regenerate plan (if generator present) and push live.
cd "$(dirname "$0")" || exit 1

# 1. Regenerate plan.json from your generator, if it's here
if [ -f build_plan.py ]; then
  python3 build_plan.py && echo "↻ plan.json regenerated" || echo "⚠️  build_plan.py failed — pushing existing files"
fi

# 2. Keep the deployed app file in sync with the source
[ -f canyon-forge.html ] && cp canyon-forge.html index.html

# 3. Commit + push
git add -A
if git diff --cached --quiet; then
  echo "✓ nothing changed — already up to date"
  exit 0
fi
git commit -m "Update ${1:-plan} $(date '+%Y-%m-%d %H:%M')" >/dev/null
git push origin main && echo "✅ pushed — live at your Pages URL in ~1 min"
