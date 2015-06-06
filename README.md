# Paradox Calculator

Paradox Calculator is a machine-learning command-line utility written in Python that determines a ChallengePost project's chances at winning. It uses a ChallengePost Scraper created in conjunction with the project to fetch data from ChallengePost. It was built at HackRPI, a hackathon hosted at RPI (Rensselaer Polytechnic Institute). You can view the project on ChallengePost [here](http://challengepost.com/software/paradox-calculator).

The scraper was used for gathering past winning project data for training Paradox Calculator to predict a project's chances of winning. The scraper is also written in Python 3 and runs with Anaconda. It uses the numpy and scipy modules for training the program. This project served as an interesting look into the realm of machine learning. I worked on the scraper for gathering test data and my teammate worked on the machine learning component. I later integrated some of his code with my scraper to allow us to input a ChallengePost project's URL. The utility outputs the chances of the project winning based on the algorithm we put together.

## Future Plans

It would be preferrable to use an existing API to fetch project data. However, no API existed at the time of this project. ChallengePost's GitHub account shows that there is an authentication API under development. After talking with ChallengePost staff, it seems that the developers are also working on an API for project data. In the meantime, this utility will serve in the place of an API.

## Project Authors

- Taylor Foxhall ([@hallfox](https://github.com/hallfox))
- Alan Plotko ([@alanplotko](https://github.com/alanplotko))
