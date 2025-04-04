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

# 获取aiOS窗口位置
get_window_position() {
    osascript <<EOD
tell application "System Events"
    set appWindow to first window of (first process whose name contains "aiOS")
    set {x, y} to position of appWindow
    set {width, height} to size of appWindow
    return {x, y, width, height}
end tell
EOD
}

# 定义点击函数
click_at() {
    osascript -e "tell application \"System Events\" to click at {$1, $2}"
}

# 截取屏幕特定区域
capture_screen() {
    # 在窗口中心位置截取200x200的区域
    local x=$1
    local y=$2
    local center_x=$((x + 150))
    local center_y=$((y + 150))
    screencapture -R"$center_x,$center_y,200,200" "temp.png"
}

# 主循环
echo "监控已启动，按Control+C停止..."

while true; do
    # 获取窗口位置
    window_info=$(get_window_position)
    if [ $? -eq 0 ]; then
        # 解析窗口信息
        read x y width height <<< $(echo $window_info | tr ',' ' ')
        
        # 截取窗口中心区域
        capture_screen $x $y
        
        # 比较图片
        if sips -g all "temp.png" | grep -q "disconnected.png"; then
            echo "✓ 检测到断开连接，尝试重连..."
            # 点击截图区域中心
            click_at $((x + 250)) $((y + 250))
            sleep 2
        fi
        
        # 删除临时截图
        rm -f "temp.png"
    fi
    
    # 等待间隔
    sleep 0.5
done 