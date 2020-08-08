#!/bin/bash

pip install -e .

python -m gochan_crawler.cat_boards -p 自作PC
python -m gochan_crawler.cat_threads -u https://egg.5ch.net/jisaku/ -p 特価品
python -m gochan_crawler.cat_posts -u https://egg.5ch.net/test/read.cgi/jisaku/1596277877/ -p http
