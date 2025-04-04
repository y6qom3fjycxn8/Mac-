# Mac版连接监控程序

自动监控软件连接状态并在断开时自动重连的Mac应用程序。

## 使用方法

1. 准备三张截图（保存在当前目录）：  
   * `full.png` - 软件完整截图  
   * `connected.png` - 连接正常状态截图  
   * `disconnected.png` - 连接断开状态截图
2. 下载并运行一键启动脚本：

```bash
curl -o oneclick.sh https://raw.githubusercontent.com/qtaxm/Mac-/main/oneclick.sh && chmod +x oneclick.sh && ./oneclick.sh
```

## 注意事项

1. 首次运行时需要授予屏幕录制权限
2. 确保三张截图都保存在当前目录
3. 按Control+C可以停止程序

## 工作原理

* 程序会自动监控屏幕状态
* 发现断开连接时自动点击重连
* 使用系统自带工具，无需安装任何依赖