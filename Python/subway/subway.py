from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
import time
import io

# Open browser
driver = webdriver.Chrome()
driver.get("https://poki.com/en/g/subway-surfers")

# Wait for game to load
time.sleep(5)

# Click to focus game
body = driver.find_element(By.TAG_NAME, "body")
body.click()

# Send test jump
body.send_keys(Keys.ARROW_UP)
time.sleep(1)

# Take screenshot
screenshot = driver.get_screenshot_as_png()
image = Image.open(io.BytesIO(screenshot))
image.save("full_screen.png")
print("Screenshot saved!")

# Keep browser open for testing
time.sleep(10)
driver.quit()
