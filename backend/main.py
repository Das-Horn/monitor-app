import systemScraper
import threading
import time
running = True


def scrape_loop():
    local_settings = settings.get_settings()
    print(local_settings)
    while running:
        while local_settings['enabled']:
            scrape.set_copy(settings.get_settings())
            time.sleep(local_settings['scrape_interval'])
            scrape.scrape_data()
            local_settings = settings.get_settings()
        local_settings = settings.get_settings()
    return

def main():
    scrape.set_copy(settings.get_settings())
    scrape_thread = threading.Thread(target=scrape_loop)
    scrape_thread.start()
    scrape_thread.join()
    return

if __name__ == "__main__":
    settings = systemScraper.settings()
    scrape = systemScraper.scraper()
    main()