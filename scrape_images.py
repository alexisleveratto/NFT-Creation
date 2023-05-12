import os

from selenium import webdriver
import configparser
import requests
import bs4
import time


class WebScrape:
    def __init__(self, config: configparser):
        self.driver = webdriver.Chrome(config["WEB"]["chrome_driver_path"])
        self.folder_path = config["WEB"]["folder_name"]

        if not os.path.isdir(self.folder_path):
            os.makedirs(self.folder_path)

    def download_images(self, url, num):
        response = requests.get(url)

        if response.status_code == 200:
            with open(
                os.path.join(self.folder_path, "image-{}.jpg".format(num)), "wb"
            ) as file:
                file.write(response.content)

    def download(self, *look_for):
        query = ""
        for word in look_for:
            query += "{}+".format(word)

        search_url = "http://www.google.com/search?q={}&source=lnms&tbm=isch".format(
            query[:-1]
        )

        self.driver.get(search_url)

        wait = input("Scroll until finished ... ")

        self.driver.execute_script("window.scrollTo(0, 0);")

        page_html = self.driver.page_source
        page_soup = bs4.BeautifulSoup(page_html, "html.parser")
        containers = page_soup.findAll("div", {"class": "isv-r PNCib MSM1fd BUooTd"})

        print(len(containers))

        len_containers = len(containers)

        for i in range(1, len_containers + 1):
            if i % 25 == 0:
                continue

            x_path = """//*[@id="islrg"]/div[1]/div[{}]""".format(i)

            preview_image_x_path = (
                """//*[@id="islrg"]/div[1]/div[{}]/a[1]/div[1]/img""".format(i)
            )
            preview_image_element = self.driver.find_element(
                "xpath", preview_image_x_path
            )
            preview_image_url = preview_image_element.get_attribute("src")

            self.driver.find_element("xpath", x_path).click()
            time.sleep(1)

            time_started = time.time()
            while True:

                image_element = self.driver.find_element(
                    "xpath",
                    """//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img""",
                )
                image_url = image_element.get_attribute("src")

                if image_url != preview_image_url:
                    break
                else:
                    current_time = time.time()

                    if current_time - time_started > 11:
                        print(
                            "Timeout! Will download a lower resolution image and move onto the next one"
                        )
                        break

            # Downloading image
            try:
                self.download_images(image_url, i)
                print(
                    "Downloaded element {} out of {} total".format(
                        i, len_containers + 1
                    )
                )
            except:
                print(
                    "Couldn't download an image {}, continuing downloading the next one".format(
                        i
                    )
                )
