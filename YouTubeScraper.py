from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import argparse


class YouTubeScraper:
    def __init__(self, channel_id, driver_path, output_file=None, headless=True, delay=1.1, strip_special_characters=False):
        self.channel_id = channel_id
        self.output_file = output_file
        self.delay = delay
        self.strip_special_characters = strip_special_characters
        self.videos = []
        self.driver = None
        self.driver_path = driver_path
        self.headless = headless

    def __init_driver(self):
        if self.headless:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            self.driver = webdriver.Chrome(
                executable_path=self.driver_path, options=options)

        else:
            self.driver = webdriver.Chrome(
                executable_path=self.driver_path)

        self.driver.get(
            f'https://www.youtube.com/channel/{self.channel_id}/videos')

        # wait for page to load
        wait = WebDriverWait(self.driver, 10)

    def __scroll(self):
        last_height = 0
        current_height = self.driver.execute_script(
            "return document.documentElement.scrollHeight")

        # continuously scroll down page until all videos are loaded

        while last_height != current_height:
            last_height = current_height

            # wait for body tag to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located(
                (By.TAG_NAME, 'body')))

            # scroll down page
            self.driver.find_element(
                By.TAG_NAME, 'body').send_keys(Keys.END)

            time.sleep(self.delay)

            # update page height
            current_height = self.driver.execute_script(
                "return document.documentElement.scrollHeight")

    def __get_videos(self):
        self.videos = [(str(video.get_attribute("href")), str(video.get_attribute("title")))
                       for video in self.driver.find_elements(By.ID, 'video-title-link')]

        # strip special characters from titles
        if self.strip_special_characters:
            self.videos = [(video[0], self.__strip_special_characters(
                video[1])) for video in self.videos]

    def __strip_special_characters(self, title):
        new_title = title
        new_title = new_title.replace('/', '')
        new_title = new_title.replace(':', '')
        new_title = new_title.replace('(', '')
        new_title = new_title.replace(')', '')
        new_title = new_title.replace('?', '')
        new_title = new_title.replace('!', '')
        new_title = new_title.replace('*', '')
        new_title = new_title.replace('"', '')
        new_title = new_title.replace('<', '')
        new_title = new_title.replace('>', '')
        new_title = new_title.replace('|', '')
        new_title = new_title.replace('\'', '')
        new_title = new_title.replace(',', '')
        new_title = new_title.replace('&amp', 'and')
        new_title = new_title.replace('&#39;', '')
        new_title = new_title.replace('&quot;', '')
        new_title = new_title.replace('\u2013', '')

        new_title = new_title.strip()

        return new_title

    def __write_to_file(self):
        video_count = 0
        with open(self.output_file, 'w') as f:
            f.write('"URL","Title"\n')
            for video in self.videos:
                try:
                    f.write(
                        f'"{video[0]}","{video[1]}"\n')
                    video_count += 1
                except:
                    print(f'Error writing {video[1]}, {video[0]} to file.')

        print(f'Wrote {video_count} videos to file.')

    def scrape(self):
        self.__init_driver()
        self.__scroll()
        self.__get_videos()

        if self.output_file:
            self.__write_to_file()

        self.driver.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('channel_id', help='YouTube channel ID',
                        type=str)
    parser.add_argument('driver', help='Path to chromedriver executable',
                        type=str)
    parser.add_argument('-o', '--output', help='Output file name/path',
                        type=str, required=False, metavar='OUTPUT_FILE')
    parser.add_argument('-delay', '--delay',
                        help='Delay between page loads', type=float, required=False, default=1.1)
    parser.add_argument('-strip', '--strip',
                        help='Strip special characters', required=False, default=False, action='store_true')
    parser.add_argument('-head', '--head',
                        help='Run driver without headless mode', required=False, default=True, action='store_false')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    scraper = YouTubeScraper(args.channel_id, args.driver, output_file=args.output,
                             delay=args.delay, strip_special_characters=args.strip, headless=args.head)

    scraper.scrape()


if __name__ == '__main__':
    exit(main())
