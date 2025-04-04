#!/bin/bash

# 获取用户桌面路径
DESKTOP="$HOME/Desktop"

# 下载运行脚本
curl -o "$DESKTOP/run.sh" https://raw.githubusercontent.com/qtaxm/Mac-/main/run.sh

# 添加执行权限
chmod +x "$DESKTOP/run.sh"

# 运行脚本
"$DESKTOP/run.sh" 