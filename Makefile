clean:
	find . -type f -name "*.pyc" -exec rm {} \;

crawl-bmkg:
	scrapy crawl bmkg -L WARNING

crawl-gdacs-eq:
	scrapy crawl gdacs -L WARNING -a event_type=EQ

crawl-gdacs-fl:
	scrapy crawl gdacs -L WARNING -a event_type=FL

crawl-gdacs-tc:
	scrapy crawl gdacs -L WARNING -a event_type=TC

crawl-gdacs: crawl-gdacs-eq crawl-gdacs-fl crawl-gdacs-tc

crawl-all: crawl-gdacs crawl-bmkg
