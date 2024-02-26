import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import keyboard
import pyperclip


class InstagramBot:
    def __init__(self, massage):
        self.massage = massage
        self.__driver = self.__setup_web_driver()

    def __setup_web_driver(self):
        return webdriver.Chrome()

    def __pause(self):
        time.sleep(random.randrange(2, 6))

    def __xpath(self, path):
        xpath = WebDriverWait(self.__driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, path))
        )
        return xpath

    def __pres_entr(self):
        pyperclip.copy(self.massage)
        keyboard.press_and_release('ctrl+v')
        keyboard.press_and_release('enter')

    def login_bot(self, username, password):
        self.__driver.get('https://www.instagram.com/')
        self.__pause()

        try:
            input_user_name = WebDriverWait(self.__driver, 10).until(
                ec.presence_of_element_located((By.NAME, 'username'))
            )
            input_password = WebDriverWait(self.__driver, 10).until(
                ec.presence_of_element_located((By.NAME, 'password'))
            )

            input_user_name.send_keys(username)
            input_password.send_keys(password)
            input_password.send_keys(Keys.ENTER)

            WebDriverWait(self.__driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search"]'))
            )
        except Exception as e:
            print(f"Error during login: {str(e)}")

    def find_user(self, target_users):

        try:
            for user in target_users:
                user_url = f'https://www.instagram.com/{user}/'
                self.__pause()
                self.__driver.get(user_url)

                button = WebDriverWait(self.__driver, 10).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'button'))
                )

                button_color = button.value_of_css_property('background-color')

                if button_color == 'rgba(0, 149, 246, 1)':
                    button.click()
                    self.__send_message()
                else:
                    self.__send_message()

        except Exception as e:
            print(f"Error finding user: {str(e)}")

    def exit(self):
        self.__driver.close()
        self.__driver.quit()

    def __send_message(self):
        try:
            self.__pause()
            self.__xpath(
                '//div[@class="x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w x972fbf xcfux6l x1qhh985 xm0m39n xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x18d9i69 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x78zum5 x1f6kntn xwhw2v2 x10w6t97 xl56j7k x17ydfre x1swvt13 x1pi30zi x1n2onr6 x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye x1gjpkn9 x5n08af xsz8vos"]'
                ).click()

        except Exception as e:
            print(f'{e}')

        try:
            self.__pause()
            self.__xpath('/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]').click()
            self.__pause()
            self.__pres_entr()
        except Exception:
            self.__pause()
            self.__pres_entr()

