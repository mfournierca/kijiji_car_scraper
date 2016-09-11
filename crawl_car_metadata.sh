#!/bin/sh

scrapy crawl nrcan_fuel_ratings_spider -o data/nrcan_fuel_ratings.csv -t csv
