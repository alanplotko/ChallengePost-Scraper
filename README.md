# ChallengePost Scraper

The ChallengePost scraper is a utility that serves to fetch project data from ChallengePost while the developers at ChallengePost build an API.

The scraper was used for gathering past winning project data to for training a program to predict a project's chances of winning. You can view the project on ChallengePost [here](http://challengepost.com/software/paradox-calculator). The scraper is written with Python 3 and is run with Anaconda. It uses the numpy and scipy modules for training the program. This project served as an interesting look into the realm of machine learning. I worked on the scraper for gathering test data and Taylor Foxhall worked on the machine learning component. I later integrated some of his code with my scraper to allow us to input project URL's and get back the chances of the project winning based on the algorithm we put together.
