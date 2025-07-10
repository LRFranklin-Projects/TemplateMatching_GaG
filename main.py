# TODO: When using this on your computer: First find you screen size and edit the screenshot size - Then edit the hardcoded lcoations for next seed and previous seed

import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui

pyautogui.PAUSE = 0

print("Press 's' to start playing.")
print("Once started press 'q' to quit.")
keyboard.wait('s')

sct = mss.mss()
screenshot_size = {
    'top': 0,
    'left': 0,
    'width': 1900,
    'height': 1000,
}


fps_time = time()

seed_cost_cent_symbol = cv2.imread('seed_cost_symbol.png', cv2.IMREAD_UNCHANGED)
if seed_cost_cent_symbol.shape[2] == 4:
    seed_cost_cent_symbol = cv2.cvtColor(seed_cost_cent_symbol, cv2.COLOR_BGRA2BGR)

buy_cost_cent_symbol = cv2.imread('buy_cost_symbol.png', cv2.IMREAD_UNCHANGED)
if buy_cost_cent_symbol.shape[2] == 4:
    buy_cost_cent_symbol = cv2.cvtColor(buy_cost_cent_symbol, cv2.COLOR_BGRA2BGR)

shop_leave_x_symbol = cv2.imread('shop_leave_symbol.png', cv2.IMREAD_UNCHANGED)
if shop_leave_x_symbol.shape[2] == 4:
    shop_leave_x_symbol = cv2.cvtColor(shop_leave_x_symbol, cv2.COLOR_BGRA2BGR)

shop_teleport_seeds_symbol = cv2.imread('shop_teleport_symbol.png', cv2.IMREAD_UNCHANGED)
if shop_teleport_seeds_symbol.shape[2] == 4:
    shop_teleport_seeds_symbol = cv2.cvtColor(shop_teleport_seeds_symbol, cv2.COLOR_BGRA2BGR)

buying_stock = False
click_found = True
current_shop = 'seeds'
seed_searching = 0

sleep(5)  # Wait for the game to load

while True:
    scr = sct.grab(screenshot_size)

    scr_np = numpy.array(scr)  # Convert to NumPy array
    scr_rgb = scr_np[:, :, :3]  # Remove alpha channel

    if not buying_stock and click_found:
        w = seed_cost_cent_symbol.shape[1]
        h = seed_cost_cent_symbol.shape[0]

        result = cv2.matchTemplate(scr_rgb, seed_cost_cent_symbol, cv2.TM_CCOEFF_NORMED)
        
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        print(f"Max Val: {max_val} Max Loc: {max_loc}")

        src = scr_np.copy()

        print(f'Match for SEED symbol: {max_val}')
        if max_val > .75:
            x = max_loc[0] + w // 2
            y = max_loc[1] + h // 2
            # Draw rectangle on screen
            frame = scr_rgb.copy()
            #cv2.rectangle(frame, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
            #cv2.imshow('Screen Shot', frame)
            cv2.waitKey(1)
            pyautogui.moveTo(x, y, duration=.5)
            pyautogui.click(x=x, y=y)
            print('Clicking seed to open up buy menu')
            click_found = True
            buying_stock = True
            sleep(3)
        elif seed_searching < 25:
            print('Click not found for SEED symbol')
            click_found = True
            buying_stock = False
            seed_searching += 1
            pyautogui.moveTo(956, 808, duration=.5)  # Move to next seed button
            pyautogui.click(x=956,y=808)
            print('Inside SEED click: Clicking to next seed since stock is out')
            sleep(3)
        else: 
            print('Went through entire shop list, sending to reset')
            click_found = False
            seed_searching += 5



    elif buying_stock and click_found:
        w = buy_cost_cent_symbol.shape[1]
        h = buy_cost_cent_symbol.shape[0]

        result = cv2.matchTemplate(scr_rgb, buy_cost_cent_symbol, cv2.TM_CCOEFF_NORMED)
        
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        print(f"Max Val: {max_val} Max Loc: {max_loc}")

        src = scr_np.copy()

        print(f'Match for STOCK buy symbol: {max_val}')
        if max_val > .57:
            buying_stock = True
            x = max_loc[0] + w // 2
            y = max_loc[1] + h // 2
            # Draw rectangle on screen
            frame = scr_rgb.copy()
            #cv2.rectangle(frame, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
            #cv2.imshow('Screen Shot', frame)
            cv2.waitKey(1)
            pyautogui.moveTo(x, y, duration=.5)
            pyautogui.click(x=x, y=y)
            print('Clicking to buy STOCK')
            sleep(.5)
        else:
            buying_stock = False
            pyautogui.moveTo(956, 808, duration=.5)
            pyautogui.click(x=956,y=808)
            print('Inside STOCK buy: Clicking to next seed since stock is out')
            sleep(3)

    elif not click_found and not buying_stock and seed_searching >= 25:
        w = shop_leave_x_symbol.shape[1]
        h = shop_leave_x_symbol.shape[0]

        # Resetting to top of shop
        print('Resetting shop')
        for i in range(25):
            pyautogui.moveTo(938, 340, duration=.5)
            pyautogui.click(x=938, y=340)
            sleep(1)
            if keyboard.is_pressed('q'):
                cv2.destroyAllWindows()
                var = 0/0 # Cause error to end program
        print('Shop reset')
        seed_searching = 0

        result = cv2.matchTemplate(scr_rgb, shop_leave_x_symbol, cv2.TM_CCOEFF_NORMED)
        
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        print(f"Max Val: {max_val} Max Loc: {max_loc}")

        src = scr_np.copy()

        print(f'Match for red x symbol: {max_val}')
        if max_val > .57:
            buying_stock = False
            x = max_loc[0] + w // 2
            y = max_loc[1] + h // 2
            # Draw rectangle on screen
            frame = scr_rgb.copy()
            #cv2.rectangle(frame, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
            #cv2.imshow('Screen Shot', frame)
            cv2.waitKey(1)
            pyautogui.moveTo(x, y, duration=.5)
            pyautogui.click(x=x, y=y)
            print('Clicking red x')
            sleep(5)

        if current_shop == 'seeds':
            current_shop == 'tools'
            keyboard.press_and_release('2')
            sleep(1)
            pyautogui.moveTo(700, 700, duration=.5)
            pyautogui.click(x=700, y=700)
            sleep(2)
            keyboard.press_and_release('e')
            sleep(5)
            pyautogui.moveTo(1187, 565, duration=.5)
            pyautogui.click(x=1187, y=565)
            sleep(3)
            # Fix here
        
        elif current_shop == 'tools':
            w = shop_teleport_seeds_symbol.shape[1]
            h = shop_teleport_seeds_symbol.shape[0]

            result = cv2.matchTemplate(scr_rgb, shop_teleport_seeds_symbol, cv2.TM_CCOEFF_NORMED)
            
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            print(f"Max Val: {max_val} Max Loc: {max_loc}")

            src = scr_np.copy()

            print(f'Match for seed shop teleport symbol: {max_val}')
            if max_val > .57:
                buying_stock = True
                x = max_loc[0] + w // 2
                y = max_loc[1] + h // 2
                # Draw rectangle on screen
                frame = scr_rgb.copy()
                #cv2.rectangle(frame, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
                #cv2.imshow('Screen Shot', frame)
                cv2.waitKey(1)
                pyautogui.moveTo(x, y, duration=.5)
                pyautogui.click(x=x, y=y)
                print('Clicking seeds shop teleport')
                sleep(3)
            
            keyboard.press_and_release('e')
            sleep(3)
            # Incorporate shop open

        # Resetting variables
        click_found = True
        buying_stock = False


    if keyboard.is_pressed('q'):
        cv2.destroyAllWindows()
        break

    print('FPS: {}'.format(1 / (time() - fps_time)))
    fps_time = time()