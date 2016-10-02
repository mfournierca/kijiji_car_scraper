#!/bin/sh

NAMES=("kijiji" "ottawahonda" "tonygrahamtoyota" "jimtubman" "caronauto" "belairlexustoyota")

for name in "${NAMES[@]}"
do
    OUTPUT=data/${name}_cars.csv
    SPIDER=${name}_car_spider
    mv $OUTPUT ${OUTPUT}.bak
    scrapy crawl $SPIDER -o $OUTPUT -t csv
done
