from pynput.mouse import Controller
import time
import random
import logging
from smoose import get_curve

# time settings
inactiveMin = 2
inactiveMaxShiftSec = 30

# mouse move area settings
minX = minY = 50
maxX = maxY = 1000
random_shift = 100

logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")

mouse = Controller()
mouse_pos = mouse.position
random.seed()
logging.info("Process started... Inactive time set as {} minutes plus up to {} sec at random. Current mouse pos is {}"
             .format(inactiveMin, inactiveMaxShiftSec, mouse_pos))

while True:

    time.sleep(inactiveMin*60 + random.uniform(0, inactiveMaxShiftSec))
    logging.info("Checking if mouse has been moved: \n\t Remembered position is {} \n\t Current position is {}"
                 .format(mouse_pos, mouse.position))

    if mouse_pos == mouse.position:
        logging.info("Starting to move mouse...")
        points = list()
        new_points = mouse.position
        for i in range(random.randint(50, 100)):
            new_points = (new_points[0] + random.uniform(-random_shift, random_shift),
                          new_points[1] + random.uniform(-random_shift, random_shift)
                          )
            new_points = ((new_points[0] if new_points[0] > minX else random.uniform(minX, minX + random_shift)),
                          (new_points[1] if new_points[1] > minY else random.uniform(minY, minY + random_shift))
                          )
            new_points = ((new_points[0] if new_points[0] < maxX else random.uniform(maxX - random_shift, maxX)),
                          (new_points[1] if new_points[1] < maxY else random.uniform(maxY - random_shift, maxY))
                          )
            points.append(new_points)

        for curveXY in get_curve(points):
            mouse.position = curveXY
            time.sleep(random.uniform(0, 0.01))

        logging.info("Moving stopped")
    else:
        logging.info("Mouse has been moved since last check. Skipping loop step...")
    mouse_pos = mouse.position

