from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("⚠️ webdriver_manager not found. Using default ChromeDriver path.")
    ChromeDriverManager = None

from PIL import Image
import numpy as np
import cv2
import io
import time
import sys
import traceback

def run_subway_surfers_bot():
    driver = None
    retry_count = 0
    max_retries = 3
    
    while retry_count < max_retries:
        try:
            # Launch browser with better options
            options = Options()
            options.add_argument("--start-maximized")  # Ensure full window
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
            options.add_argument("--no-sandbox")  # Bypass OS security model
            options.add_argument("--disable-gpu")  # Applicable to Windows OS only
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_experimental_option("useAutomationExtension", False)
            
            # Initialize Chrome with appropriate driver
            if ChromeDriverManager:
                try:
                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=options)
                except Exception as e:
                    print(f"⚠️ WebDriver manager failed: {e}")
                    # Fallback to default driver
                    driver = webdriver.Chrome(options=options)
            else:
                # Use default driver if manager not available
                driver = webdriver.Chrome(options=options)
            
            # Set page load timeout
            driver.set_page_load_timeout(30)
            print(f"🌐 Opening browser (attempt {retry_count+1}/{max_retries})...")
            
            # Navigate to the game
            driver.get("https://poki.com/en/g/subway-surfers")
        
        print("📱 Loading Subway Surfers...")
        
        # Handle cookie popup if it appears
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cmp-button_button.cmp-intro_acceptAll"))
            ).click()
            print("🍪 Cookie notice accepted")
        except (TimeoutException, NoSuchElementException):
            print("🍪 No cookie notice found, continuing")
        
        # Wait for canvas to load
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "pixi-canvas")))
            print("🎮 Game canvas found")
        except TimeoutException:
            # Try alternative canvas selectors if ID fails
            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas.pixi-canvas")))
                print("🎮 Game canvas found (alternative selector 1)")
            except TimeoutException:
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))
                    print("🎮 Game canvas found (any canvas)")
                except TimeoutException:
                    print("❌ Could not find game canvas after multiple attempts")
                    raise
            
        # Wait additional time for assets to load
        time.sleep(8)
        
        # Focus the game and find canvas (using more robust selector)
        canvas = None
        canvas_found = False
        
        # Try multiple selector strategies
        selectors = [
            (By.ID, "pixi-canvas"),
            (By.CSS_SELECTOR, "canvas.pixi-canvas"),
            (By.CSS_SELECTOR, "canvas#gameCanvas"),
            (By.CSS_SELECTOR, "div.game-container canvas"),
            (By.TAG_NAME, "canvas")
        ]
        
        for selector_type, selector_value in selectors:
            try:
                canvas = driver.find_element(selector_type, selector_value)
                canvas_found = True
                print(f"🎮 Found canvas using: {selector_value}")
                break
            except NoSuchElementException:
                continue
        
        if not canvas_found:
            print("❌ Failed to find game canvas with any selector")
            raise NoSuchElementException("Game canvas not found")
        
        # Ensure game is focused and loaded
        try:
            # Try to click middle of canvas for best results
            action = webdriver.ActionChains(driver)
            action.move_to_element(canvas).click().perform()
            print("🎯 Game focused with action chain")
        except:
            # Fallback to simple click
            try:
                canvas.click()
                print("🎯 Game focused with direct click")
            except:
                print("⚠️ Could not click canvas, trying to continue anyway")
        
        print("⏳ Waiting for game to initialize...")
        time.sleep(5)  # Give more time for game to initialize
        
        # Try multiple methods to start the game
        try:
            # Method 1: Direct key to canvas
            canvas.send_keys(Keys.ARROW_UP)
            print("🎲 Attempted game start with direct key")
            time.sleep(1)
            
            # Method 2: Action chains for more reliable key sending
            action = ActionChains(driver)
            action.move_to_element(canvas).click().send_keys(Keys.ARROW_UP).perform()
            print("🎲 Attempted game start with action chain")
            
            # Method 3: Send to active element
            driver.switch_to.active_element.send_keys(Keys.ARROW_UP)
            print("🎲 Attempted game start with active element")
            
            time.sleep(2)  # Wait longer for game to start
            
            # Some games need space bar to start
            canvas.send_keys(Keys.SPACE)
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Game activation attempt had an issue: {e}")
            print("⏩ Continuing anyway...")
        
        # Game control variables
        last_action_time = time.time()
        action_cooldown = 0.5  # Prevent too frequent actions
        consecutive_jumps = 0
        max_consecutive_jumps = 3
        
        # Game Loop: Read canvas repeatedly
        for i in range(100):  # Increased to 100 cycles
            # Take screenshot and process with error handling
            try:
                screenshot = driver.get_screenshot_as_png()
                img = Image.open(io.BytesIO(screenshot))
            except WebDriverException as e:
                print(f"❌ Screenshot error: {e}")
                print("🔄 Attempting to recover...")
                time.sleep(1)
                continue
                
            # Get canvas location and size with error handling
            try:
                loc = canvas.location
                size = canvas.size
                left = loc['x']
                top = loc['y']
                right = left + size['width']
                bottom = top + size['height']
            except (WebDriverException, AttributeError) as e:
                print(f"❌ Canvas location error: {e}")
                print("🔄 Attempting to relocate canvas...")
                try:
                    # Try to find canvas again
                    try:
                        canvas = driver.find_element(By.ID, "pixi-canvas")
                    except NoSuchElementException:
                        try:
                            canvas = driver.find_element(By.CSS_SELECTOR, "canvas.pixi-canvas")
                        except NoSuchElementException:
                            # Last resort - try any canvas
                            canvas = driver.find_element(By.TAG_NAME, "canvas")
                    canvas.click()
                    continue
                except Exception:
                    print("❌ Failed to relocate canvas")
                    break
            
            # Crop to canvas only
            try:
                canvas_img = img.crop((left, top, right, bottom))
                canvas_img = canvas_img.resize((960, 540))  # Standard size
            except (ValueError, SystemError) as e:
                print(f"Error cropping image: {e}. Retrying...")
                time.sleep(1)
                continue
                
            # Convert to opencv format and process
            frame = np.array(canvas_img)
            
            # Convert BGR to RGB if needed
            if frame.shape[2] == 4:  # If RGBA
                frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
            
            # Create grayscale for obstacle detection
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            
            # Define multiple ROIs to detect obstacles at different distances
            # Near obstacles (for jumps)
            near_roi = gray[380:430, 470:490]  # Directly in front of character
            
            # Side obstacles (for lane changes)
            left_roi = gray[380:430, 440:460]   # Left side check
            right_roi = gray[380:430, 500:520]  # Right side check
            
            # Detect obstacles in each region
            near_obstacle = np.mean(near_roi) < 100  # Darker areas are obstacles
            left_obstacle = np.mean(left_roi) < 100
            right_obstacle = np.mean(right_roi) < 100
            
            current_time = time.time()
            can_act = current_time - last_action_time > action_cooldown
            
            # Decision logic with cooldown
            if can_act:
                if near_obstacle:
                    if consecutive_jumps < max_consecutive_jumps:
                        print(f"🚨 Frame {i+1}: Obstacle ahead! Jumping!")
                        canvas.send_keys(Keys.ARROW_UP)
                        consecutive_jumps += 1
                        last_action_time = current_time
                    else:
                        # Too many consecutive jumps, try lane change
                        if left_obstacle and not right_obstacle:
                            print(f"🚨 Frame {i+1}: Changing lane right!")
                            canvas.send_keys(Keys.ARROW_RIGHT)
                        elif not left_obstacle and right_obstacle:
                            print(f"🚨 Frame {i+1}: Changing lane left!")
                            canvas.send_keys(Keys.ARROW_LEFT)
                        else:
                            # If no clear path, jump anyway
                            print(f"🚨 Frame {i+1}: No clear path! Jumping!")
                            canvas.send_keys(Keys.ARROW_UP)
                        consecutive_jumps = 0
                        last_action_time = current_time
                else:
                    # Path is clear, reset consecutive jumps
                    consecutive_jumps = 0
                    print(f"✅ Frame {i+1}: Path clear!")
            
            # Visualize what the bot sees
            # Draw ROIs
            cv2.rectangle(frame, (470, 380), (490, 430), (0, 255, 0), 2)  # near
            cv2.rectangle(frame, (440, 380), (460, 430), (255, 0, 0), 2)  # left
            cv2.rectangle(frame, (500, 380), (520, 430), (0, 0, 255), 2)  # right
            
            # Add status text
            obstacle_text = "Obstacle!" if near_obstacle else "Clear"
            cv2.putText(frame, f"Status: {obstacle_text}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
            # Show visualization
            cv2.imshow("Subway Surfers Bot View", frame)
            key = cv2.waitKey(1) & 0xFF
            
            # Press 'q' to quit
            if key == ord('q'):
                print("❌ User quit")
                break
                
            # Adjust sleep time based on game speed - shorter for more responsive controls
            time.sleep(0.1)
            
        except WebDriverException as e:
            print(f"❌ WebDriver error: {e}")
            retry_count += 1
            
            # Cleanup before retry
            try:
                if driver:
                    driver.quit()
            except:
                pass
            
            print(f"🔄 Retrying ({retry_count}/{max_retries})...")
            time.sleep(3)  # Wait before retry
            continue
            
        except TimeoutException:
            print("⏱️ Page load timed out. Retrying...")
            retry_count += 1
            
            # Cleanup before retry
            try:
                if driver:
                    driver.quit()
            except:
                pass
                
            print(f"🔄 Retrying ({retry_count}/{max_retries})...")
            time.sleep(3)
            continue
            
        except Exception as e:
            print(f"❌ Error occurred: {str(e)}")
            break
            
        # If we get here without exceptions, break the retry loop
        break
            
    # If we've exhausted all retries
    if retry_count >= max_retries:
        print(f"❌ Failed after {max_retries} attempts. Please check your connection and try again.")
    
    # Final cleanup
    print("🛑 Bot stopped. Cleaning up...")
    try:
        cv2.destroyAllWindows()
    except:
        pass
    try:
        if driver:
            driver.quit()
    except:
        pass
    print("✅ Done!")

if __name__ == "__main__":
    run_subway_surfers_bot()