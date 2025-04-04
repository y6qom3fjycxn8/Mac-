# Mac版连接监控程序

自动监控软件连接状态并在断开时自动重连的Mac应用程序。

## 系统要求

- Python 3.6 或更高版本
- pip3 包管理器

## 安装步骤

1. 安装依赖：
```bash
pip3 install -r requirements.txt
```

2. 准备模板图片：
- `disconnected.png` - 连接断开状态的截图

## 使用方法

1. 一键安装运行：
```bash
curl -L https://raw.githubusercontent.com/qtaxm/Mac-/main/monitor_connection.py -o monitor_connection.py && curl -L https://raw.githubusercontent.com/qtaxm/Mac-/main/requirements.txt -o requirements.txt && curl -L https://raw.githubusercontent.com/qtaxm/Mac-/main/disconnected.png -o disconnected.png && pip3 install -r requirements.txt && python3 monitor_connection.py
```

2. 按照提示操作：
   - 将鼠标移动到断开连接开关的位置
   - 等待3秒记录位置
   - 按回车开始监控

## 注意事项

1. 首次运行时需要授予辅助功能权限
2. 按F12可以停止监控
3. 保持监控区域可见，不要遮挡

## 工作原理

- 程序会自动监控屏幕状态
- 发现断开连接时自动点击重连
- 使用OpenCV进行图像匹配，准确率更高