import numpy as np
import matplotlib.pyplot as plt 
import random

HEIGHT = 50
WIDTH = 50

def get_camera_frame(frame_type):
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    for row in range(HEIGHT):
        for col in range(WIDTH):

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

            frame[row, col] = [r, g, b]
    return frame

def classify_frame(frame):
    red_pixel_count = 0
    blue_pixel_count = 0
    gray_pixel_count = 0
    total_pixels = HEIGHT * WIDTH

    for row in range(HEIGHT):
        for col in range(WIDTH):
            r, g, b = map(int,frame[row, col])

            if r > 200 and g < 100 and b < 100:
                red_pixel_count += 1
            elif b > 200 and r < 100 and g < 100:
                blue_pixel_count += 1
            elif abs(r - g) < 10 and abs(g - b) < 10: 
                gray_pixel_count += 1

    red_density = (red_pixel_count / total_pixels) * 100
    blue_density = (blue_pixel_count / total_pixels) * 100
    gray_density = (gray_pixel_count / total_pixels) * 100

    match True:
        case _ if red_density > 60:
            label = "RED OBJECT"
        case _ if blue_density > 60:
            label = "BLUE OBJECT"
        case _ if gray_density > 60:
            label = "GRAY OBJECT"
        case _:
            label = "NO OBJECT"

    return label, red_density, blue_density, gray_density

for color in ["red", "blue", "gray"]:
    image = get_camera_frame(color)
    label, red_d, blue_d, gray_d = classify_frame(image)

    print("Classification Result:",label)
    print("Red Density:",red_d,"% |",
           "Blue Density:",blue_d,"% |",
           "Gray Density:",gray_d,"%"
    )

    plt.imshow(image)
    plt.title(
        label+"\n"+
        "Red: " + str(red_d) + "% | " +
        "Blue: " + str(blue_d) + "% | " +
        "Gray: " + str(gray_d) + "%"
)
    plt.axis("off")
    plt.show()
