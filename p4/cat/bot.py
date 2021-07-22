import os
import time
from stat import S_ISREG, ST_CTIME, ST_MODE

from selenium import webdriver                        
from selenium.webdriver.firefox.options import Options as FirefoxOptions

jobs_folder = 'bot_stuff'#config.sys.argv[2]
old_jobs_folder = 'bot_old'#sys.argv[3]

options = FirefoxOptions()
options.add_argument("--headless")

while True:
    entries = (os.path.join(jobs_folder, fn) for fn in os.listdir(jobs_folder))
    entries = ((os.stat(path), path) for path in entries)
    entries = ((stat[ST_CTIME], path) for stat, path in entries if S_ISREG(stat[ST_MODE]))

    for _, path in sorted(entries)[::-1]:
        with open(path, 'r') as f:
            url = f.read()

        print('Processing {}'.format(url))

        os.rename(path, old_jobs_folder+'/'+os.path.basename(path))

        driver = webdriver.Firefox(options=options, firefox_binary='firefox/firefox', executable_path='./geckodriver')
        try:
            driver.set_page_load_timeout(4)
            driver.get(url)
            time.sleep(4)
        except Exception as e:
            print(e)
        finally:
            driver.quit()

    time.sleep(5)
