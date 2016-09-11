#!/bin/sh

scrapy crawl caronauto_car_spider -o data/caronauto_cars.csv -t csv
scrapy crawl kijiji_car_spider -o data/kijiji_cars.csv -t csv
scrapy crawl ottawahonda_car_spider -o data/ottawahonda_cars.csv -t csv
scrapy crawl tonygrahamtoyota_car_spider -o data/tonygrahamtoyota_cars.csv -t csv
scrapy crawl jimtubman_car_spider -o data/jimtubman_cars.csv -t csv
