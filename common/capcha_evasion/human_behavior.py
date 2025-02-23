import random
import time

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def human_pause(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))


# Function to simulate mouse movement towards an element
def human_like_move_to_element(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element).pause(random.uniform(0.5, 1.5)).perform()


# Function to safely find an element (without stopping the script if not found)
def find_element_safe(driver, by, value, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(ec.presence_of_element_located((by, value)))
    except (NoSuchElementException, TimeoutException):
        print(f"Element not found: {value}")
        return None
