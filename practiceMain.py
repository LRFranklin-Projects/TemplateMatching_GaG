import cv2
import numpy as np
import mss #screenshots
import pyautogui
from time import time, sleep

game_img = cv2.imread('game_example_screen.png', cv2.IMREAD_UNCHANGED)
in_stock_img = cv2.imread('seed_cost_symbol.png', cv2.IMREAD_UNCHANGED)
buy_stock_img = cv2.imread('buy_cost_symbol.png', cv2.IMREAD_UNCHANGED)

#cv2.imshow('game', game_img)
#cv2.waitKey()
#cv2.destroyAllWindows()

#cv2.imshow('seed_stock_symbol', in_stock_img)
#cv2.waitKey()
#cv2.destroyAllWindows()

result = cv2.matchTemplate(game_img, in_stock_img, cv2.TM_CCOEFF_NORMED)

#cv2.imshow('Result', result)
#cv2.waitKey()
#cv2.destroyAllWindows()

# Value is the best/worst match and location is the location of it
min_val, max_Val, min_loc, max_loc = cv2.minMaxLoc(result)
print(max_loc)
print(max_Val)

width = in_stock_img.shape[1]
height = in_stock_img.shape[0]

# To create rectangle you input: image to create on, top left point(max_loc), bottom right point(add w/h of img to max_loc), border color, border width
#cv2.rectangle(game_img, max_loc, (max_loc[0] + width, max_loc[1] + height), (0, 255, 255), 2)

#cv2.imshow('game', game_img)
#cv2.waitKey()
#cv2.destroyAllWindows()

threshold = .85
yloc, xloc = np.where(result >= threshold)
#print(len(xloc)) # Shows that it finds 5 in_stock cent symbols

# Creating all rectangles that meet threshold of 85%  confidence
#for (x, y) in zip(xloc, yloc):
    #cv2.rectangle(game_img, (x,y), (x+width, y+height), (0, 255, 255), 2)

#cv2.imshow('game', game_img)
#cv2.waitKey()
#cv2.destroyAllWindows()

# Create a rectangles list using top left x, top left y, width, and height
rectangles = []
# Add each found match location to the rectangles list
for (x, y) in zip(xloc, yloc):
    # Add each twice to ensure there is 2 for when grouping
    rectangles.append([int(x), int(y), int(width), int(height)])
    rectangles.append([int(x), int(y), int(width), int(height)])

# Input how many you want in group: 1 - and - how close they have to be to be in a group: 0.2
rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
print(len(rectangles))

for (x, y, w, h) in rectangles:
    cv2.rectangle(game_img, (x,y), (x+w, y+h), (0, 255, 255), 2)

cv2.imshow('game', game_img)
cv2.waitKey()
cv2.destroyAllWindows()