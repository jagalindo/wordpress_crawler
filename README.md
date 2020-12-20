#wordpress_crawler
This is a simple wordpress crawler wrtitten in python

It also supports Docker enviroment for execution

docker build . -t wp_crawl
docker run --rm -v repopath/data:/data wp_crawl 2> /dev/null

