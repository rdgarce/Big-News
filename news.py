import requests
from datetime import datetime
from json import dumps, loads

class WNAfetcher:
    
    def __init__(self, apikey : str):
        
        self._apikey = apikey
        self._next_article = 0
        self._total_num_articles = 0xffffffff #Initial very high value. Updated on each query
        self._fetch_config = {
            'language': None,
            'text': None,
            'source_countries': None,
            'min_sentiment': None,
            'max_sentiment': None,
            'earliest_publish_date': None,
            'latest_publish_date': None,
            'news_sources': None,
            'authors': None,
            'entities': None,
            'location_filter': None,
            'sort': None,
            'sort_direction': None
        }

    def get_query(self) -> dict:
        return self._fetch_config
        
    def config_query(self, language, text = None, source_countries = None,
                min_sentiment = None, max_sentiment = None, earliest_publish_date : datetime = None,
                latest_publish_date : datetime = None, news_sources = None, authors = None,
                entities = None, location_filter = None, sort = None, sort_direction = None):
        """
        Configure the instance for querying articles with the specified attributes.
        Note: Non specified parameters are set to None
        """
        self._fetch_config.update({
            'language': language,
            'text': text,
            'source_countries': source_countries,
            'min_sentiment': min_sentiment,
            'max_sentiment': max_sentiment,
            'earliest_publish_date': earliest_publish_date,
            'latest_publish_date': latest_publish_date,
            'news_sources': news_sources,
            'authors': authors,
            'entities': entities,
            'location_filter': location_filter,
            'sort': sort,
            'sort_direction': sort_direction
        })

    def reset_offset(self):
        """
        The fetching will start again from the top of the queried articles list.
        """
        self._next_article = 0
        self._total_num_articles = 0xffffffff #Initial very high value. Updated on each query

    def load_config(self, file_name = "WNAfetcher.cfg"):
        with open(file_name, "r") as file:
            config = loads(file.read())
            self._next_article = config['next_article']
            self._total_num_articles = config['total_num_articles']
            self._fetch_config = config['fetch_config']
            self._fetch_config['earliest_publish_date'] = \
                datetime.strptime(self._fetch_config['earliest_publish_date'], "%Y-%m-%d")
            self._fetch_config['latest_publish_date'] = \
                datetime.strptime(self._fetch_config['latest_publish_date'], "%Y-%m-%d")

    def persist_config(self, file_name = "WNAfetcher.cfg"):
        with open(file_name, "w") as file:
            config = {
                'next_article': self._next_article,
                'total_num_articles': self._total_num_articles,
                'fetch_config': self._fetch_config
            }
            config['fetch_config']['earliest_publish_date'] = \
                config['fetch_config']['earliest_publish_date'].strftime("%Y-%m-%d")
            config['fetch_config']['latest_publish_date'] = \
                config['fetch_config']['latest_publish_date'].strftime("%Y-%m-%d")
            file.write(dumps(config))

    def _ll_fetch(self, number) -> (int, dict, dict | None):
        
        config = self._fetch_config
        assert config['language'] and number

        base_url = "https://api.worldnewsapi.com/search-news" + \
                   "?language=" + str(config['language'])     + \
                   "&offset=" + str(self._next_article)       + \
                   "&number=" + str(number)
        
        custom = ""
        if config['text'] is not None:
            custom += "&text=" + str(config['text'])
        if config['source_countries'] is not None:
            custom += "&source-countries=" + str(config['source_countries'])
        if config['min_sentiment'] is not None:
            custom += "&min-sentiment=" + str(config['min_sentiment'])
        if config['max_sentiment'] is not None:
            custom += "&max-sentiment=" + str(config['max_sentiment'])
        if config['earliest_publish_date'] is not None:
            custom += "&earliest-publish-date=" + config['earliest_publish_date'].strftime("%Y-%m-%d")
        if config['latest_publish_date'] is not None:
            custom += "&latest-publish-date=" + config['latest_publish_date'].strftime("%Y-%m-%d")
        if config['news_sources'] is not None:
            custom += "&news-sources=" + str(config['news_sources'])
        if config['authors'] is not None:
            custom += "&authors=" + str(config['authors'])
        if config['entities'] is not None:
            custom += "&entities=" + str(config['entities'])
        if config['location_filter'] is not None:
            custom += "&location-filter=" + str(config['location_filter'])
        if config['sort'] is not None:
            custom += "&sort=" + str(config['sort'])
        if config['sort_direction'] is not None:
            custom += "&sort-direction=" + str(config['sort_direction'])
        
        full_url = base_url + custom
        response = requests.get(full_url, headers={'x-api-key': self._apikey})

        sc = response.status_code
        headers = response.headers
        try:
            return sc, headers, response.json()
        except:
            return sc, headers, None

    def fetch_batch(self, batch_size: int) -> list | None:
        """
        Returns a list of articles consisting of min(batch_size,100) elements
        or None if you have no more credits.
        """
        if self._next_article >= self._total_num_articles:
            return []

        sc, _, bd = self._ll_fetch(batch_size)

        if sc != 200 or bd is None:
            return None

        self._total_num_articles = bd['available']
        self._next_article += bd['number']

        return bd['news']
    
    def standardize(self, articles : list) -> list:
        """
        Standardize the give articles list to be compliant to ARTICLE INTERFACE
        """
        std_articles = []
        if articles is None:
            return std_articles
        
        for a in articles:
            std_articles.append(
                {
                "title": a['title'],
                "link": a['url'],
                "date": a['publish_date'],
                "text": a['text']
                }
            )
        
        return std_articles