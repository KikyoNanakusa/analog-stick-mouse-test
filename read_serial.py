import serial
from pynput.mouse import Controller, Button
import time

mouse = Controller()
ser = serial.Serial('COM7', 9600)  

x_center, y_center = 502, 520
# x_center, y_center = 0, 0

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

touch_pressed = False
mode = "mouse"  # 最初のモードをマウスモードとして設定
switch_ready_to_toggle = True  # スイッチがモード切替の準備ができているかどうかを追跡するフラグ

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            try:
                x, y, analog_switch, touch = map(int, data.split(','))
                # if x_center == 0 and y_center == 0:
                #     while x > 600:
                #         continue
                #     x_center, y_center = x, y
                #     print("Center point set to:", x_center, y_center)
                x = x - x_center
                y = y - y_center
                # スケーリングを適用
                x_move = map_value(x, -512, 512, -10, 10)
                y_move = map_value(y, -512, 512, -10, 10)
                
                # スイッチの値に基づいてモード切替
                if y > -200:    # 動作安定のため
                    if analog_switch <= 10 and switch_ready_to_toggle:
                        mode = "scroll" if mode == "mouse" else "mouse"
                        print("Mode switched to:", mode)
                        switch_ready_to_toggle = False  # 切替後はフラグをオフにする
                    elif analog_switch > 10:
                        switch_ready_to_toggle = True  # スイッチの値が10を超えたら再度切替可能

                if mode == "mouse":
                    # マウス移動
                    mouse.move(x_move, y_move)
                    # タッチセンサーの状態をチェック
                    if touch > 650:
                        if not touch_pressed:
                            mouse.press(Button.left)
                            touch_pressed = True
                    else:
                        if touch_pressed:
                            mouse.release(Button.left)
                            touch_pressed = False
                elif mode == "scroll":
                    # スクロール操作
                    mouse.scroll(0, -y_move / 5)

            except ValueError:
                print("Received malformed data. Ignoring...")
            time.sleep(0.01)
except KeyboardInterrupt:
    print("Program terminated.")
    ser.close()
