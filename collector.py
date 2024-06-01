from datetime import datetime, timedelta
from redis import Redis
import os
from news import WNAfetcher
from article import ATCqueue

if __name__ == "__main__":
    
    wna_api = os.getenv("COLLECTOR_WNA_API")
    redis_host = os.getenv("COLLECTOR_REDIS_HOST")
    redis_port = os.getenv("COLLECTOR_REDIS_PORT")
    redis_psw = os.getenv("COLLECTOR_REDIS_PASSWORD")
    if not wna_api or not redis_host or not redis_port or not redis_psw:
        exit(-1)
    redis_port = int(redis_port)
    
    queue = ATCqueue(
        Redis(host=redis_host, port=redis_port, password=redis_psw)
    )
    fetcher = WNAfetcher(wna_api)

    one_day = timedelta(days=1)

    try:
        fetcher.load_config()
    except:
        # If load fails we start again fetching news from today and going back
        fetcher.reconfig(language="it",
                            earliest_publish_date = datetime.now().date() - one_day,
                            latest_publish_date = datetime.now().date())

    while (articles := fetcher.fetch_batch()) != None:
        articles = fetcher.standardize(articles)
        print(f"LOG: Extracted {len(articles)} articles")
        q_len = queue.push_batch(articles)
        print(f"LOG: Reliable article queue now has {q_len} elements")

        fetcher._fetch_config['earliest_publish_date'] = \
            fetcher._fetch_config['earliest_publish_date'] - one_day
        fetcher._fetch_config['latest_publish_date'] = \
            fetcher._fetch_config['latest_publish_date'] - one_day
        
        fetcher.persist_config()
    print("No more credits. Exiting... Call me in 24h :D")