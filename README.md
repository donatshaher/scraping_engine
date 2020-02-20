# scraping_engine

An automated housing classifieds scraper which finds the hottest deals. Kijiji never surfaces hottest deals - so this script finds them for you. 

How do we define hottest deals? hotness rank = "visits / time elapsed since ad was posted"


THE PROCESS:

All you have to provide is the starting search URL - by starting URL I mean say that you searched for "apartments in Toronto" -  the resultant search query will be the starting search URL. This is where you do all the filtering on kijiji (ex: price = x, location=y, etc). kijiji URL will incorporate all of these filtering options.

Then, you also provide number of pages you want to iterate and the oldest ad you're willing to tolerate. Then the script outputs a list of listings and their ranks. The higher the rank of the listing, the 'hotter" it is'.




HOW IS IT IMPLEMENTED?

Kijiji has a metric called "visits" for each ad. To find the most popular items for your search query (which might return 1000s of results)- you'd have to go through on very item for page 1,2,3, etc. Then you'd have to look at visits and tiemstamp of each ad. Then compare all of them.

Instead, the scraper will do this and scrape all items on all corresponding pages, calculate a "hotness" metric, which is "visits / time elapsed since ad was posted". Then it will sort the listings from hottest to least hot.
