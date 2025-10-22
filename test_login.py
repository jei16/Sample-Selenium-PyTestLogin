from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pytest
import time
import os
from datetime import datetime

class TestLogin:
    @pytest.fixture()
    def test_setup(self):
        """Setup Chrome driver before test and close it after."""
        global driver
        options = Options()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        driver.maximize_window()
        yield
        driver.close()
        driver.quit()

    def test_login(self, test_setup):
        """Test valid/invalid login on OrangeHRM demo site."""
        driver.get("https://opensource-demo.orangehrmlive.com/")

        # Create folders if they don't exist
        os.makedirs("successful_screenshots", exist_ok=True)
        os.makedirs("failed_screenshots", exist_ok=True)

        # Enter credentials (try changing username/password to test failure)
        username = "Admin"
        password = "admin123"
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        time.sleep(3)  # Allow time for page transition

        # Create a timestamp for screenshot naming
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        try:
            # Verify if Dashboard appears
            dashboard_text = driver.find_element(By.XPATH, "//h6[text()='Dashboard']").text

            assert "Dashboard" in dashboard_text
            print("✅ Login successful! Dashboard is visible.")

            screenshot_path = f"successful_screenshots/login_successful_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")

        except Exception as e:
            # If Dashboard not found → login failed
            print("❌ Login failed! Dashboard not found.")
            screenshot_path = f"failed_screenshots/login_failed_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")

            # Try to capture visible error message
            try:
                error_text = driver.find_element(By.XPATH, "//p[contains(@class, 'oxd-alert-content-text')]").text
                print(f"⚠️ Error message shown: {error_text}")
            except:
                print("⚠️ No visible error message found.")

            print("Error details:", e)
