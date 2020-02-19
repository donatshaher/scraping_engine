# scraping_engine

An automated housing classified scraper which finds hottest deals

All you have to provide is the starting search URL - by starting URL I mean say that you searched for "apartments in Toronto" -  the resultant search query will be the starting search URL.

Kijiji has a metric called "visits" but it doesn't surface the hottest deals. To find the most popular items for your search query (which might return 1000s of results)- you'd have to go through on very item for page 1,2,3, etc

Instead, the scraper will scrape all items on all corresponding pages, calculate a "hotness" metric, which is "visits / time elapsed since ad was posted". Then it will sort the listings from hottest to least hot. And, the results will be shown.
