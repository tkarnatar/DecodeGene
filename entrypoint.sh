#!/bin/sh
set -e

# Render 等平台會注入 $PORT，預設 80（docker-compose 用）
PORT="${PORT:-80}"
sed -i "s/listen 80;/listen ${PORT};/" /etc/nginx/conf.d/default.conf

exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
