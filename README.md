# ChallengePost Scraper

The ChallengePost Scraper is a utility that serves to fetch project data from ChallengePost. It was built for the Paradox Calculator project completed at HackRPI, a hackathon hosted at RPI (Rensselaer Polytechnic Institute). You can view the project on ChallengePost [here](http://challengepost.com/software/paradox-calculator).

The scraper was used for gathering past winning project data for training Paradox Calculator to predict a project's chances of winning. The scraper is written with Python 3 and runs with Anaconda. It uses the numpy and scipy modules for training the program. This project served as an interesting look into the realm of machine learning. I worked on the scraper for gathering test data and my teammate worked on the machine learning component. I later integrated some of his code with my scraper to allow us to input a ChallengePost project's URL. The utility outputs the chances of the project winning based on the algorithm we put together.

## Future Plans

After talking with ChallengePost staff, it seems that the developers are working on an API. In the meantime, this utility will serve in the place of an API.
