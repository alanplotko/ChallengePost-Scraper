import urllib3
import os
import time
import datetime
from lxml import html
import re
import sys
from collections import defaultdict
import Stemmer
import numpy as np
import math
import random

class Project:
	def __init__(self, name, description="", tags=[], numLikes=0, numHackers=0, hasVideo=0, winner=0):
		self.name = name
		self.desc = description
		self.tags = tags
		self.likes = numLikes
		self.hackers = numHackers
		self.video = hasVideo
		self.winner = winner

PATH = os.getcwd() + "\\"
PATH_FOLDER = ""
http = urllib3.PoolManager()

stemmer = Stemmer.Stemmer("english")
keywords = list(map(stemmer.stemWord, ["data", "application", "time", "user", "information", "people", "game", "want", "get", "make"]))
tags = ["web", "android", "javascript", "ios", "windows", "hardware", "mac", "java", "css", "python"]
FEATURES = 24

def runScraper(query):
	url = 'http://challengepost.com/software/search?page='
	pageMax = int(input("How many pages to search for: "))
	print("\n")
	startProgress("Scraping ChallengePost")
	for i in range(1, pageMax + 1):
		new_url = url + str(i) + "&query=" + query
		request = http.request('GET', new_url)
		if request.status == 200:
			with open(PATH_FOLDER + 'files\\cp' + str(i) + '.txt', 'w', encoding='utf-8') as fout:
				fout.write(request.data.decode('utf-8'))
			progress((i / pageMax) * 100)
		else:
			print("Max page number is " + str(i - 1))
			return

def grabLinks(folderName):
	fileList = os.listdir(PATH_FOLDER + "\\files\\")
	size = len(fileList)
	if not os.path.exists(PATH_FOLDER + 'links.txt'):
		with open(PATH_FOLDER + 'links.txt', 'w', encoding='utf-8') as fout:
			pass
	for i in range(0, size):
		file = open(PATH_FOLDER + "\\files\\" + fileList[i], encoding='utf-8').read()
		tree = html.fromstring(file)
		links = tree.xpath('//a[@class="block-wrapper-link fade link-to-software"]/@href')
		if (len(links) != 24):
			print("Problem with " + fileList[i])
		with open(PATH_FOLDER + 'links.txt', 'a',  encoding='utf-8') as fout:
			for link in links:
				fout.write(link + "\n")
			print("Grabbed 24 links from " + fileList[i])

def grabProjects(folderName):
	url = 'http://challengepost.com/'

	if not os.path.exists(PATH_FOLDER + 'links.txt'):
		print("Missing links.txt file")
		return

	numLines = sum(1 for line in open(PATH_FOLDER + 'links.txt'))
	with open(PATH_FOLDER + 'links.txt', 'r', encoding='utf-8') as fin:
		fileList = os.listdir(PATH_FOLDER + "\\files\\")
		startProgress("Downloading projects")
		for i, line in enumerate(fin.readlines()):
			new_url = url + line.rstrip()
			if not os.path.exists(PATH_FOLDER + 'projects\\' + line.rstrip().replace("/software/", "") + '.txt'):
				request = http.request('GET', new_url)
				if request.status == 200:
					tree = html.fromstring(request.data.decode('utf-8'))		
					winnerBadges = tree.xpath('//span[@class="winner label radius small all-caps"]')
					if (len(winnerBadges) == 0):
						with open(PATH_FOLDER + 'projects\\' + line.rstrip().replace("/software/", "") + '.txt', 'w', encoding='utf-8') as fout:
							fout.write(request.data.decode('utf-8'))
					progress((i / numLines) * 100)
	print("\n")

def getData(folder1, folder2):
	fileList1 = os.listdir(PATH + folder1 + "\\projects\\")
	fileList2 = os.listdir(PATH + folder2 + "\\projects\\")
	size1 = math.floor(0.25 * len(fileList1))
	size2 = math.floor(0.75 * len(fileList2))
	files1 = random.sample(fileList1, size1)
	files2 = random.sample(fileList2, size2)
	files1.extend(files2)
	total = len(files1)

	if not os.path.exists(PATH + '\\data\\'):
		os.makedirs(PATH + '\\data\\')
	projects = []
	startProgress("Getting project data")
	for i in range(0, total):
		if i < size1:
			file = open(PATH + folder1 + "\\projects\\" + str(files1[i]), encoding='utf-8').read()
		else:
			file = open(PATH + folder2 + "\\projects\\" + str(files1[i]), encoding='utf-8').read()
		tree = html.fromstring(file)
		p = Project(name=files1[i].replace(".txt", ""))
		
		# Has video
		videos = tree.xpath('//div[@class="flex-video"]')
		if len(videos) > 0:
			p.video = 1
		else:
			p.video = 0

		# Number of hackers
		p.hackers = len(tree.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " software-team-members ")]'))

		# Description
		try:
			p.desc = tree.xpath('//article[@id="app-details"]//div/p/text()[normalize-space()]')[0].encode('ascii', 'ignore').decode('utf-8')
			if re.search('[a-zA-Z]', p.desc) == None:
				p.desc = ""
		except IndexError or UnicodeEncodeError:
			continue

		# Likes
		p.likes = len(tree.xpath('//ul[@class="like-users"]/li'))

		# Tags
		p.tags = tree.xpath('//ul[@id="app-labels"]//a/text()')

		# Winner
		if i < size1:
			p.winner = 1
		else:
			p.winner = 0

		projects.append(p)

		progress((i / total) * 100)

	print("\n")

	return projects

def analyzeData(projects, analyze):
	dKeywords = defaultdict(int)
	dTags = defaultdict(int)
	X = np.array([])
	y = np.zeros(len(projects))

	global keywords, tags, stemmer, FEATURES

	if analyze == 1:

		for project in projects:
			project.desc = "".join(stemmer.stemWord(c) for c in project.desc if c.isalnum() or c.isspace()).split()
			for word in project.desc:
			    dKeywords[word] += 1
			for tag in project.tags:
				dTags[tag] += 1

		if not os.path.exists(PATH + '\\data\\frequency-keywords.txt'):
			with open(PATH + '\\data\\frequency-keywords.txt', 'w', encoding='utf-8') as fout:
				pass

		if not os.path.exists(PATH + '\\data\\frequency-tags.txt'):
			with open(PATH + '\\data\\frequency-tags.txt', 'w', encoding='utf-8') as fout:
				pass	

		with open(PATH + '\\data\\frequency-keywords.txt', 'w',  encoding='utf-8') as fout:
		    for w in sorted(dKeywords, key=dKeywords.get, reverse=True):
		    	fout.write(str(w) + ": " + str(dKeywords[w]) + "\n")

		with open(PATH + '\\data\\frequency-tags.txt', 'w',  encoding='utf-8') as fout:
		    for w in sorted(dTags, key=dTags.get, reverse=True):
		    	fout.write(str(w) + ": " + str(dTags[w]) + "\n")

	for i, project in enumerate(projects):
		#winner
		y[i] = project.winner

		#create example
		example = np.zeros(FEATURES)
			
		#video
		example[0] = project.video
		
		#num hackers
		example[1] = project.hackers
		
		#num likes
		example[2] = project.likes

		#10 keywords
		for i, k in enumerate(keywords):
			if k in project.desc:
				example[i + 3] = 1

		#num tags
		example[13] = len(project.tags)

		#10 tags
		for i, k in enumerate(tags):
			if k in project.tags:
				example[i + 14] = 1

		X = np.append(X, example)
		#print(example)
	print(np.size(X), len(projects), FEATURES)
	print()
	X = np.reshape(X, (len(projects), FEATURES))

	if analyze != 2:
		np.savez("training_data.npz", X=X, y=y)
		return 1
	else:
		return X

def parseProject(url):
	global PATH

	request = http.request('GET', url)
	name = url.split("/software/")[1]
	currentStep = 1
	totalSteps = 7

	if request.status == 200:
		with open(PATH + 'projects\\' + name + '.txt', 'w', encoding='utf-8') as fout:
			fout.write(request.data.decode('utf-8'))

	projects = []
	startProgress("Getting project data")
	file = open(PATH + "\\projects\\" + name + ".txt", encoding='utf-8').read()
	
	tree = html.fromstring(file)
	p = Project(name=name)
		
	# Has video
	videos = tree.xpath('//div[@class="flex-video"]')
	if len(videos) > 0:
		p.video = 1
	else:
		p.video = 0

	currentStep += 1
	progress((currentStep / totalSteps) * 100)

	# Number of hackers
	p.hackers = len(tree.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " software-team-members ")]'))
	
	currentStep += 1
	progress((currentStep / totalSteps) * 100)

	# Description
	try:
		p.desc = tree.xpath('//article[@id="app-details"]//div/p/text()[normalize-space()]')[0].encode('ascii', 'ignore').decode('utf-8')
		if re.search('[a-zA-Z]', p.desc) == None:
			p.desc = ""
	except IndexError or UnicodeEncodeError:
		pass

	currentStep += 1
	progress((currentStep / totalSteps) * 100)

	# Likes
	p.likes = len(tree.xpath('//ul[@class="like-users"]/li'))

	currentStep += 1
	progress((currentStep / totalSteps) * 100)

	# Tags
	p.tags = tree.xpath('//ul[@id="app-labels"]//a/text()')

	currentStep += 1
	progress((currentStep / totalSteps) * 100)

	# Winner
	winnerBadges = tree.xpath('//span[@class="winner label radius small all-caps"]')
	
	if len(winnerBadges) > 0:
		p.winner = 1
	else:
		p.winner = 0

	currentStep += 1
	progress((currentStep / totalSteps) * 100)

	projects.append(p)

	currentStep += 1
	progress((currentStep / totalSteps) * 100)

	print("\n")

	return analyzeData(projects, 2)

def startProgress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x - progress_x))
    sys.stdout.flush()
    progress_x = x

def endProgress():
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()

def main():
	global PATH, PATH_FOLDER

	if input("Query (0) or url (anything else): ") == "0":
		query = input("\nType query: ")
	else:
		name = input("\nType url: http://challengepost.com/sofware/")
		parseProject(name)
		return

	folderName = query.replace(":", "-") + "-" + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
	PATH_FOLDER = PATH + folderName + "\\"
	print("\nChecking for folder " + folderName)
	
	try:
		if not os.path.exists(folderName + "\\files"):
			os.makedirs(PATH_FOLDER + "\\files")
		else:
			print("Files folder exists!")

		if not os.path.exists(PATH + "projects"):
			os.makedirs(PATH + "projects")
		else:
			print("Individual projects folder exists!")	

		if not os.path.exists(folderName + "\\projects"):
			os.makedirs(PATH_FOLDER + "\\projects")
		else:
			print("Projects folder exists!")

		if not os.path.exists(folderName):
			os.makedirs(PATH_FOLDER)
			print("Created folder " + folderName)
		else:
			print("Folder " + folderName + " already exists. Grabbing links!")

	except OSError:
		print("Error: Cannot create directory\n")

	if input("Scrape ChallengePost (y)? : ").lower() == "y":
		print("Running scraper...")
		runScraper(query)

	if input("Extract links (y)? : ").lower() == "y":
		print("Running link grabber...")
		grabLinks(folderName)

	if input("Get projects (y)? : ").lower() == "y":
		print("Running project grabber...")
		grabProjects(folderName)

	if input("Extract data (y)? : ").lower() == "y":
		print("Running data extraction tool...")
		projects = getData("is-winner-2014-11-16", "-2014-11-16")
		result = analyzeData(projects, input("Analyze data (1): "))

if __name__ == '__main__':
	main()