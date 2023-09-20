import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import emails

# Replace 'path/to/chromedriver' with the path to your downloaded WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)

# Replace 'https://example.com' with the URL of the web page you want to interact with
initial_url = "https://tickets.mhaifafc.com/he-IL/events/stade%20rennais%20fc%20-%20maccabi%20haifa%20fc/2023-9-21_18.45/roazhon%20park?hallmap"

try:
    while True:
        driver.get(initial_url)
        print(initial_url)
        # Find all <area> elements within the <map>
        component_loaded = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "div.imageContainerRow map area",
                )
            )
        )
        area_elements = driver.find_elements(
            By.CSS_SELECTOR, "div.imageContainerRow map area"
        )

        # Initialize count for clickable areas
        clickable_area_count = 0

        # Iterate through each <area> element
        for i in range(len(area_elements)):
            # Find the <area> element again to avoid staleness
            time.sleep(2)
            area_element = driver.find_elements(
                By.CSS_SELECTOR,
                "div.imageContainerRow map area",
            )[i]

            # Click on the <area> element
            area_element.click()

            # Check if the URL has changed (indicating a redirect)
            if driver.current_url != initial_url:
                clickable_area_count += 1
                last_area = area_element
                driver.back()
                time.sleep(2)
                # Perform additional checks or actions if needed
            else:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "div.ui-dialog-buttonset button",
                        )
                    )
                )
                error_button = driver.find_element(
                    By.CSS_SELECTOR,
                    "div.ui-dialog-buttonset button",
                )
                error_button.click()
                time.sleep(2)
                background = driver.find_element(By.CSS_SELECTOR, "body.body_css")
                background.click()

        # Based on the count, take action
        if clickable_area_count == 1:
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "div.imageContainerRow map area",
                    )
                )
            )
            area_elements = driver.find_elements(
                By.CSS_SELECTOR,
                "div.imageContainerRow map area",
            )
            print(len(area_elements))

            for j in range(len(area_elements)):
                # Find the <area> element again to avoid staleness
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            "div.imageContainerRow map area",
                        )
                    )
                )
                area_element = driver.find_elements(
                    By.CSS_SELECTOR,
                    "div.imageContainerRow map area",
                )[j]
                print(j)
                time.sleep(2)

                # Click on the <area> element
                area_element.click()

                # Check if the URL has changed (indicating a redirect)
                print(driver.current_url)
                print(initial_url)
                if driver.current_url == initial_url:
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                "div.ui-dialog-buttonset button",
                            )
                        )
                    )
                    error_button = driver.find_element(
                        By.CSS_SELECTOR,
                        "div.ui-dialog-buttonset button",
                    )
                    error_button.click()
                    time.sleep(5)
                    background = driver.find_element(
                        By.CSS_SELECTOR,
                        "body.body_css",
                    )
                    background.click()
                else:
                    time.sleep(2)
                    input_box = driver.find_element(
                        By.CSS_SELECTOR,
                        "div.ops span input",
                    )
                    time.sleep(2)
                    input_box.clear()  # Clear existing text if any
                    input_box.send_keys("1")
                    add_to_cart_button = driver.find_element(
                        By.CSS_SELECTOR,
                        "div.proceed a",
                    )
                    time.sleep(2)
                    add_to_cart_button.click()

                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                "span.CountDownRemainingTimeValueRegular",
                            )
                        )
                    )
                    print("sending emails")
                    ######Sending email###########
                    sending_message = emails.html(
                        html="<strong>" + "aaaaaaa" + "</strong>",
                        subject="aaaaaaaaaaaaaaaaa",
                        mail_from="admin@aicc.omsdev.in",
                    )
                    r = sending_message.send(
                        to="david0220anderson@gmail.com",
                        smtp={
                            "host": "email-smtp.us-east-1.amazonaws.com",
                            "port": 587,
                            "timeout": 5,
                            "user": "AKIATMNPWMMT4MMVDUFO",
                            "password": "BKW1oI0a+Dq8MgAK7HOoHzxSrpIvqROpynwl47WD9xV4",
                            "tls": True,
                        },
                    )
                    print("email sent")
                    break
        else:
            # Repeat the full process by refreshing the web page
            continue

        # Check if there is only one available area, if yes, break the loop
        if clickable_area_count == 1:
            break

    while True:
        pass
except Exception as e:
    raise e
finally:
    # Close the browser when done
    driver.quit()
