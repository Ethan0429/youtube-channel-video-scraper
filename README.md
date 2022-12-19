# YouTube Channel-Video Scraper

## About

This is a simple script that scrapes a YouTube channel for all the videos on the channel. It uses Selenium to scroll through the channel page, and then parses the HTML to get the video URLs and titles.

## Requirements

* Python 3.6+
* Selenium

### Pip

All requirements are listed in `requirements.txt`, and can be installed with `pip install -r requirements.txt`

### Poetry

Alternatively, you can use [Poetry](https://python-poetry.org/) to install the dependencies. To do so, run `poetry install` in the project directory, as the dependencies are listed in `pyproject.toml`.

## Usage

There are two ways to use this script. The first is to run it directly from the command line, and the second is to import it into your own project.

### CLI/Args

```
usage: YouTubeScraper.py [-h] [-o OUTPUT_FILE] [-delay DELAY] [-strip] [-head] channel_id driver
```

#### Help
```
usage: YouTubeScraper.py [-h] [-o OUTPUT_FILE] [-delay DELAY] [-strip] [-head] channel_id driver

positional arguments:
  channel_id            YouTube channel ID
  driver                Path to chromedriver executable

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        Output file name/path
  -delay DELAY, --delay DELAY
                        Delay between page loads
  -strip, --strip       Strip special characters
  -head, --head         Run driver without headless mode
```

In total there are 6 arguments, only 2 of which are required.

#### Required

* `channel_id` - The YouTube channel ID. This can be found in the URL of the channel, or by using the [YouTube Data API](https://developers.google.com/youtube/v3/docs/channels/list).
* `driver` - The path to the chromedriver executable. This can be downloaded from [here](https://chromedriver.chromium.org/downloads).

#### Optional

* `-o OUTPUT_FILE, --output OUTPUT_FILE` - The output file name/path. If not specified, then the objects will be stored in `YouTubeScraper.videos`.
* `-delay DELAY, --delay DELAY` - The delay between page scrolls. Pretty minimal, but can be useful if you're browser is loading slow. Default is 1.1 seconds which seems to work fine for me.
* `-strip, --strip` - Strip special characters from the video titles. This is useful if you're planning on using the output in a CSV file. Doesn't cover all bases, but it does the job for me. I don't recommend you use it since it's not perfect, AND it's mostly for my own purposes.
* `-head, --head` - Run the driver without headless mode. Useful for debugging.

#### Example

```bash
python3 YouTubeScraper.py UC_x5XG1OV2P6uZZ5FSM9Ttw chromedriver -o output.csv -delay 1.5 -head
```

#### Poetry Example

```bash
poetry run python3 YouTubeScraper.py UC_x5XG1OV2P6uZZ5FSM9Ttw chromedriver -o output.csv
```

### API

The script can also be imported into your own project. The `YouTubeScraper` class is the main class. It has one exposed method, `scrape`. It takes all the arguments listed in [CLI/Args](#Help), and returns a list of `Video` objects.

#### Example

```python
from YouTubeScraper import YouTubeScraper
from selenium import webdriver

channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw" # YouTube channel ID
driver_path = "chromedriver" # Path to chromedriver executable

scraper = YouTubeScraper(channel_id, driver) # Create a new scraper object
scraper.scrape() # Scrape the channel
videos = scraper.videos # Get the scraped videos
```

The `YouTubeScraper` object contains a `video` attribute, which is a list of tuples containing the video url (`video[0]`) and the video title (`video[1]`). They're both strings.
