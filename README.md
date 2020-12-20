#Wordpress Crawler
This is a simple wordpress crawler wrtitten in python

It also supports Docker enviroment for execution

``` bash
docker build . -t wp_crawl
docker run --rm -v repopath/data:/data wp_crawl 2> /dev/null
```

Also it is available as docker image at https://hub.docker.com/repository/docker/jagalindo/wp_crawler#
