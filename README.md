# WebCrawler
A web crawler that creates a site map and displays static assets


Design Decisions:

From a high level overview the program has two logical steps:
	1) Create a site map for a given url.
	2) Extract static assets from each url in the created site map.

So I created a program that had a main function that would accept a url as a command line argument and then call two functions. One for creating a site map and a second for extracting static links from a given url.

I decided that the site map generator function should also make sure the provided url was safe and should use the base domain of the provided url as a starting point every time. So I added two private subfunctions to perform these tasks.


Now that I had a general outline of the program structure I created some simple unit test cases that were failing and began working on making them pass.

(Ended up having to move the url checking and base domain finding into non-nested private functions to make unit testing easier.) - This also came in handy later on anyway.

I next began the process of building the site map and found that I should abstract the downloading of the HTML data and extracting page links from the data into their own functions. I also created a small function to make sure a list has only unique entires.

I found the logic of interating through a list while also adding to it slightly tricky (as it's best practice not to add to a list while you're iterating over it in Python). Calling unique on the list also causes the order to be randomised so that made it slightly trickier.

Parsing the html for links ended up being easier than I expected by using BeautifulSoup and then it was just a case of catching a few outliers and making sure to not add them to the list of links.

I found that there is a robots.txt file that should be respected where possible. I wrote my own methods to download and parse this robots.txt file but then found that Python had it's own class for parsing it in the standard library so I used that class instead. (wasted some time there!)

I then worked on extracting the static assets from the html. I found that I needed to extract images, js scripts and links with certain relative urls.

I improved the printing of the site_map using prettyprint.

I then worked on improving the test suite for coverage of every function.

There is a known issue with the final test of test_create_site_map due to the way that unique() returns the list in a random order the diff may fail occasionally.

Mocking out some of the calls was quite complicated in some cases.