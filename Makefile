clean:
	find . -type f -name "*.pyc" -exec rm {} \;

crawl-bmkg:
	scrapy crawl bmkg -L WARNING

crawl-gdacs:
	scrapy crawl gdacs -L WARNING

crawl-all: crawl-gdacs crawl-bmkg
