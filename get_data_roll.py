import autopy
import time
import cv2  
import numpy as np 
import os
import threading
import json 

ACTUAL_PATH = os.getcwd()

def find_similars(item, items, threshold= 10):
    new_items = list()
    for x in items:
        if sum(x)-sum(item) > threshold:
            new_items.append(x)
    return new_items

def get_screen_shot(file_name):
    # Takes the screenshot, then saves a crop where the champs gets displayed
    screen_shot = autopy.bitmap.capture_screen()
    screen_shot.save(file_name)
    image = cv2.imread(os.path.join(ACTUAL_PATH,file_name))
    crop_image = image[920:-1, 470:1480]
    cv2.imwrite("cp1_screenshot.png", crop_image) 

def identify_champ(champ_name, screenshot_name, threshold = 0.80):
    # Identifys a champ, returns the number of times the champ is in the hud
    template = cv2.imread(os.path.join(ACTUAL_PATH,'champs','images',champ_name+'.png'),0)  
    image = cv2.imread(os.path.join(ACTUAL_PATH,screenshot_name))
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)  
    w, h = template.shape[::-1]
    loc = np.where( result >= threshold)
    results_position = [x for x in zip(*loc[::-1])]
    number_of_occurrences = 0
    while len(results_position) > 0:
        results_position = find_similars(results_position[0], results_position[1:])
        number_of_occurrences += 1
    print(number_of_occurrences)
    return number_of_occurrences

def runner():
    get_screen_shot('shot.png')
    for champs in champ_list:
        identify_champ(champ+'.png','cp_screenshot.png')

if __name__ == "__main__":
    initial_time = time.time()
    with open(os.path.join(ACTUAL_PATH,'champs','data','champions.json')) as champ_data_file:
        champ_data = json.load(champ_data_file)
    # get_screen_shot('shot.png')
    champ_data.sort(key= lambda x: x['cost'])
    n = 0
    for x in champ_data:
        if identify_champ(x['champion'],'cp_screenshot.png') > 0:
            print(x)
            n +=1
        if n > 4:
            break

    # number_of_threads = 6
    # t = threading.Thread(target=identify_champ, args=('lb.png','shot.png'))
    # threads.append(t)
    # t.start()
    # t.join()
        # print(threads)
    print(time.time() - initial_time)