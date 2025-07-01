#!/bin/bash

# ブログサイト用ローカルサーバー起動スクリプト

echo "🚀 ブログサイトのローカルサーバーを起動します..."

<<<<<<< HEAD
# 現在のディレクトリ（kigyou-lab-final-main）でサーバーを起動
cd "$(dirname "$0")"
=======
# blog-siteディレクトリに移動
cd "$(dirname "$0")/blog-site"
>>>>>>> 2da2eed64906383fbc8f753aa3d0680ac5350c09

# ポート8001でHTTPサーバーを起動
echo "📡 http://localhost:8001 でサーバーを起動中..."
echo "🌐 ブラウザで http://localhost:8001 にアクセスしてください"
echo "⛔ サーバーを停止するには Ctrl+C を押してください"
echo ""

python3 -m http.server 8001