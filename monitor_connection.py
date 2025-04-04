import cv2
import numpy as np
import pyautogui
import time
from pynput import keyboard
import os
import sys


def find_aios_window():
    """查找 aios 窗口"""
    try:
        # 获取所有窗口的截图
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # 在屏幕上查找 "Disconnected" 文字所在的区域
        # 这里我们假设断开开关在窗口右上角区域
        height, width = screenshot.shape[:2]
        search_region = (width // 2, 0, width // 2, height // 2)

        # 返回一个固定的监控区域
        x = width - 400  # 距离右边 400 像素
        y = 200  # 距离顶部 200 像素
        monitor_width = 200
        monitor_height = 100
        return (x, y, monitor_width, monitor_height)
    except Exception as e:
        print(f"查找窗口时出错: {str(e)}")
        return None


def main():
    # 设置pyautogui的安全设置
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1

    print("\n监控已启动，按F12停止...")

    # 获取监控区域
    region = find_aios_window()
    if not region:
        print("错误：无法找到 aios 窗口")
        return

    print(f"将监控以下区域：")
    print(f"x={region[0]}, y={region[1]}, width={region[2]}, height={region[3]}")

    # 加载模板图片
    template = cv2.imread('disconnected.png')
    if template is None:
        print("错误：找不到模板图片 'disconnected.png'")
        return

    # 转换模板图片为灰度图
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 设置匹配阈值
    threshold = 0.3

    # 创建键盘监听器
    def on_press(key):
        if key == keyboard.Key.f12:
            print("\n停止监控")
            return False

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    print("开始监控...")
    print("提示：当前匹配阈值设置为", threshold)
    print("如果匹配不准确，可以调整 threshold 值（0.3-0.8之间）")

    try:
        while listener.running:
            try:
                # 截取屏幕指定区域
                screenshot = pyautogui.screenshot(region=region)
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

                # 模板匹配
                result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                # 打印当前匹配度
                print(f"\r当前匹配度: {max_val:.2f}", end="")

                # 如果匹配度超过阈值，执行点击
                if max_val >= threshold:
                    print(f"\n检测到断开状态，匹配度: {max_val:.2f}")
                    # 计算点击位置
                    click_x = region[0] + max_loc[0] + template.shape[1] // 2
                    click_y = region[1] + max_loc[1] + template.shape[0] // 2
                    # 执行点击
                    pyautogui.click(click_x, click_y)
                    print(f"已点击位置: x={click_x}, y={click_y}")
                    # 等待一段时间再继续监控
                    time.sleep(2)

                # 短暂延迟，避免CPU占用过高
                time.sleep(0.5)

            except Exception as e:
                print(f"\n发生错误: {str(e)}")
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n程序已停止")
    finally:
        listener.stop()


if __name__ == "__main__":
    main()