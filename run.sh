#!/bin/bash

# 获取用户桌面路径
DESKTOP="$HOME/Desktop"

# 检查是否已经安装了必要的工具
if ! command -v osascript &> /dev/null; then
    echo "错误：需要macOS系统"
    exit 1
fi

# 检查图片文件
for img in "full.png" "connected.png" "disconnected.png"; do
    if [ ! -f "$DESKTOP/$img" ]; then
        echo "错误：在桌面上找不到 $img"
        exit 1
    fi
done

# 请求屏幕录制权限
osascript <<EOD
tell application "System Events"
    if not UI elements enabled then
        display dialog "请在系统偏好设置中启用屏幕录制权限"
    end if
end tell
EOD

# 定义点击函数
click_at() {
    osascript -e "tell application \"System Events\" to click at {$1, $2}"
}

# 截取屏幕特定区域
capture_screen() {
    screencapture -R"$1,$2,$3,$4" "$DESKTOP/temp.png"
}

# 主循环
echo "监控已启动，按Control+C停止..."

while true; do
    # 截取屏幕
    capture_screen "0,0,500,400"
    
    # 使用 sips 比较图片
    if sips -g all "$DESKTOP/temp.png" | grep -q "disconnected.png"; then
        echo "检测到断开连接，尝试重连..."
        click_at "250" "200"
        sleep 2
    fi
    
    # 删除临时截图
    rm "$DESKTOP/temp.png"
    
    # 等待间隔
    sleep 1
done 