from datetime import datetime, timedelta
from redis import Redis
import os
import logging
from news import WNAfetcher
from article import ATCqueue

if __name__ == "__main__":
    logging.basicConfig(filename='collector.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s -> %(message)s',
                        datefmt= '%d/%m/%Y %H:%M:%S')
    logging.info("Starting the WNA Collector")

    wna_api = os.getenv("COLLECTOR_WNA_API")
    redis_host = os.getenv("COLLECTOR_REDIS_HOST")
    redis_port = os.getenv("COLLECTOR_REDIS_PORT")
    redis_psw = os.getenv("COLLECTOR_REDIS_PASSWORD")
    if not wna_api or not redis_host or not redis_port or not redis_psw:
        logging.error("Environment variable not defined. Exiting...")
        exit(-1)
    redis_port = int(redis_port)
    
    queue = ATCqueue(
        Redis(host = redis_host, port = redis_port, password = redis_psw)
    )
    fetcher = WNAfetcher(wna_api)

    logging.info("ATCqueue and WNAfetcher initialized successfully")

    one_week = timedelta(weeks = 1)

    try:
        fetcher.load_config()
        logging.info("Fetcher configuration loaded from file")
    except:
        # If load fails we start again fetching news from today and going back
        fetcher.config_query(language="it",
                            earliest_publish_date = datetime.now().date() - one_week,
                            latest_publish_date = datetime.now().date())
        fetcher.reset_offset()
        logging.info("Fetcher configuration not found, defaulting to a reset configuration")

    # This cicle fetches 10 news per week and then go one week back until credits end.
    # On each fetch we save the configuration so we can restart anytime
    while (articles := fetcher.fetch_batch(10)) != None:
        articles = fetcher.standardize(articles)
        query = fetcher.get_query()
        lan = query['language']
        epd = query['earliest_publish_date']
        lpd = query['latest_publish_date']
        logging.info(f"Extracted {len(articles)} articles with " +
                     f"language = {lan}, "                       +
                     f"earliest_publish_date = {epd}, "          +
                     f"latest_publish_date = {lpd}")
        
        q_len = queue.push_batch(articles)
        logging.info(f"Reliable article queue now has {q_len} elements")

        # Set epd and lpd one week in the past (10 news per week)
        epd = epd - one_week
        lpd = lpd - one_week

        fetcher.config_query(language = lan, earliest_publish_date = epd,
                                latest_publish_date = lpd)
        fetcher.reset_offset()
        fetcher.persist_config()

    logging.info("No more credits. Exiting... Call me in 24h :D")