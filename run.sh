#!/bin/bash

pip install -e .

python -m gochan_crawler.cat_board -u https://egg.5ch.net/jisaku/ -p 特価品
python -m gochan_crawler.cat_thread -u https://egg.5ch.net/test/read.cgi/jisaku/1596277877/ -p http
