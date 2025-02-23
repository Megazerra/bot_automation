import sys
import os
from common.web_driver import stop_driver, init_browser

# Agregar la carpeta raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


if __name__ == "__main__":
    try:
        driver = test_browser()
        wait = WebDriverWait(driver, 20)
        driver.get('https://nowsecure.nl')
        driver.save_screenshot('nowsecure.png')
        # Close the browser
        stop_driver(driver)
    except Exception as e:
        print(e)
