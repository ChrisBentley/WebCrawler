# WebCrawler
A web crawler that creates a site map and displays static assets


Design Decisions:

From a high level overview the program has two logical steps:
	1) Create a site map for a given url.
	2) Extract static assets from each url in the created site map.

So I created a program that had a main function that would accept a url as a command line argument and then call two functions. One for creating a site map and a second for extracting static links from a given url.

I decided that the site map generator function should also make sure the provided url was safe and should use the base domain of the provided url as a starting point every time. So I added two private subfunctions to perform these tasks.


Now that I had a general outline of the program structure I created some simple unit test cases that were failing and began working on making them pass.

(Ended up having to move the url checking and base domain finding into non-nested private functions to make unit testing easier.)