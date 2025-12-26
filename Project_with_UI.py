import numpy as np
import random
import time
from collections import deque
import requests

HEIGHT = 50
WIDTH = 50

CONVEYOR_SPEED = 1.0
DISTANCE = 2.0
DELAY = DISTANCE / CONVEYOR_SPEED

OBJECT_INTERVAL = 0.55
LATENCY_LIMIT = 0.11

total_objects = 0
red_sorted = 0
blue_sorted = 0
missed_sorts = 0

sort_queue = deque()

def get_camera_frame():
    frame_type = random.choice(["red", "blue", "gray"])
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    for row in range(HEIGHT):
        for column in range(WIDTH):

            if frame_type == "red":
                r = random.randint(150, 255)
                g = random.randint(0, 80)
                b = random.randint(0, 80)

            elif frame_type == "blue":
                r = random.randint(0, 80)
                g = random.randint(0, 80)
                b = random.randint(150, 255)

            else:   
                gray = random.randint(20, 80)
                r = g = b = gray

            frame[row][column] = [r, g, b]

    return frame

def classify_frame(frame):
    red_pixels = 0
    blue_pixels = 0
    total_pixels = HEIGHT * WIDTH

    for row in range(HEIGHT):
        for column in range(WIDTH):
            r, g, b = frame[row][column]

            if r > 180 and r > g+50 and r > b+50:
                red_pixels += 1
            elif b > 180 and b > r+50 and b > g+50:
                blue_pixels += 1

    red_density = (red_pixels / total_pixels) * 100
    blue_density = (blue_pixels / total_pixels) * 100

    match True:
        case _ if red_density > 60:
            return "RED"
        case _ if blue_density > 60:
            return "BLUE"
        case _:
            return "EMPTY"

def schedule_object(color):
    fire_time = time.time() + DELAY
    sort_queue.append((color, fire_time))
    print("[CAMERA]", color, "object scheduled")

def sorter_scheduler():
    global red_sorted, blue_sorted, missed_sorts

    if not sort_queue:
        return
    
    color, fire_time = sort_queue[0]

    if time.time() >= fire_time:
        time.sleep(0.03)

        delay_error = time.time() - fire_time

        if delay_error > LATENCY_LIMIT:
            missed_sorts += 1
            print("[SORTER] Missed due to latency")
        else:
            match color:
                case "RED":
                    red_sorted += 1
                    print("[SORTER] RED object sorted")
                case "BLUE":
                    blue_sorted += 1
                    print("[SORTER] BLUE object sorted")

        sort_queue.popleft()

def send_to_google_sheets(total, red, blue, missed):
    url = "https://script.google.com/macros/s/AKfycbwazJgDNoX8gwGZ2UftKKtWi_pJN2844p0Wb6uVp28LhW5cPxVfdMEMZIJbkiYVKGfE/exec"
    data = {"total": total, "red": red, "blue": blue, "missed": missed}
    requests.post(url, json=data)

def run_simulation(duration=60):
    global total_objects
start_time = time.time()

while time.time() - start_time < 60:

    frame = get_camera_frame()
    detected = classify_frame(frame)

    if detected in ["RED", "BLUE"]:
        total_objects += 1
        schedule_object(detected)

    loop_start = time.time()
    while time.time() - loop_start < OBJECT_INTERVAL:
            sorter_scheduler()
            time.sleep(0.08)
    
def get_stats():
    return {
        "Total Objects": total_objects,
        "Red Sorted": red_sorted,
        "Blue Sorted": blue_sorted,
        "Missed Sorts": missed_sorts
    }

print("\nPERFORMANCE REPORT")
print("Total objects processed:", total_objects)
print("Red objects sorted:", red_sorted)
print("Blue objects sorted:", blue_sorted)
print("Missed sorts:", missed_sorts)

send_to_google_sheets(total_objects, red_sorted, blue_sorted, missed_sorts)
