#!/bin/bash

# 检查是否已经安装了必要的工具
if ! command -v osascript &> /dev/null; then
    echo "错误：需要macOS系统"
    exit 1
fi

# 检查图片文件
for img in "full.png" "connected.png" "disconnected.png"; do
    if [ ! -f "$img" ]; then
        echo "错误：找不到 $img"
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
    echo "点击位置：$1, $2"
    osascript -e "tell application \"System Events\" to click at {$1, $2}"
}

# 截取屏幕特定区域
capture_screen() {
    echo "截图区域：$1,$2,$3,$4"
    screencapture -R"$1,$2,$3,$4" "temp.png"
}

# 主循环
echo "监控已启动，按Control+C停止..."
echo "正在检测断开状态..."

while true; do
    # 截取屏幕
    capture_screen "200,200,800,600"
    
    # 使用 sips 比较图片并输出结果
    echo "正在比较图片..."
    if sips -g all "temp.png" | grep -q "disconnected.png"; then
        echo "检测到断开连接，尝试重连..."
        # 调整点击位置到截图区域中心
        click_at "500" "400"
        sleep 2
    else
        echo "连接正常..."
    fi
    
    # 删除临时截图
    rm "temp.png"
    
    # 等待间隔
    sleep 3
done 