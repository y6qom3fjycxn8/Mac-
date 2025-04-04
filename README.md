# Mac版连接监控程序

## 打包步骤

1. 首先安装必要的依赖：
```bash
pip3 install py2app
pip3 install -r requirements.txt
```

2. 准备以下文件：
- `full.jpg` - 软件完整截图
- `connected.jpg` - 连接正常状态截图
- `disconnected.jpg` - 连接断开状态截图

3. 运行打包命令：
```bash
python3 setup.py py2app
```

4. 打包完成后，在 `dist` 文件夹中可以找到生成的应用程序。

## 使用说明

1. 将生成的应用程序（`连接监控.app`）复制到应用程序文件夹。

2. 首次运行时，需要授予以下权限：
   - 屏幕录制权限（用于截图）
   - 辅助功能权限（用于模拟点击）

3. 将三张模板图片放在应用程序包内：
   - 右键点击应用程序
   - 选择"显示包内容"
   - 进入 `Contents/Resources` 目录
   - 将三张图片（`full.jpg`、`connected.jpg`、`disconnected.jpg`）复制到此处

4. 运行应用程序：
   - 程序会自动检测窗口位置
   - 持续监控连接状态
   - 发现断开时自动重连
   - 按F12可以停止程序

## 注意事项

1. 确保三张模板图片清晰且具有代表性
2. 首次运行时需要设置必要的系统权限
3. 如果无法正常运行，请检查图片是否正确放置在Resources目录下 