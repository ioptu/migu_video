#!/bin/bash
# 核心业务逻辑脚本 - 保持原始逻辑版

echo "==== 开始执行抓取逻辑: $(date -u) ===="

# 1. 在主工作目录执行 Python 和下载 (对应原 steps 逻辑)
python MIGU.py || true
python sort_m3u.py || true

wget https://github.com/482349841209/rakuten-m3u-generator/raw/refs/heads/master/output/rakuten.m3u -O rkt.m3u  -t 2 --waitretry=5 || true

# 2. 提交推送阶段 (完全复刻原 CommitAndPush 逻辑)
REPO_NAME="${GITHUB_REPOSITORY#*/}"
git config --global user.email "github@github.com"
git config --global user.name "Github Actions"

# 关键：克隆到子目录
git clone "https://${GITHUB_ACTOR}:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git" "temp_repo_dir"
cd "temp_repo_dir" || exit 1 

# 从上级目录移动文件到当前子目录
[ -f "../migu.m3u" ] && mv ../migu.m3u ./migu.m3u || true
[ -f "../cctv.migu.m3u" ] && mv ../cctv.migu.m3u ./cctv.migu.m3u || true
[ -f ../rkt.m3u ] && mv ../rkt.m3u ./rakutentv.m3u || true
git add .
if git diff --cached --quiet; then
  echo "No changes to commit."
else
  git commit -m "Update: $(date -u +'%Y-%m-%d %H:%M:%S') UTC"
  git push origin main
fi

# 清理本次克隆，防止下次循环冲突
cd ..
rm -rf "temp_repo_dir"

echo "==== 逻辑执行完毕 ===="
