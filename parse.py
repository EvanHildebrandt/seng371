
import sys
import re
import os
import os.path
import time
import datetime
import dateutil.parser
import matplotlib.pyplot as plt
from numpy.random import rand
import numpy as np




def main():
	os.system('cls')
	print "Options:"
	print "		generate"
	print "		parse"
	print "		graph"
	print "		gource"
	s = raw_input('Enter an option: ')

	if s in globals():
		globals()[s]()
	else:
		print "Invalid Option"
	main()

def generate():
	#Get da logz
	print "=====Generating logs from Git Repos====="
	for item in os.listdir("../"):
		gitDir = item
		print gitDir

		if (os.path.isfile("./input/"+gitDir+"-log.txt") == False): #assume log hasnt changed since last run
			os.chdir("../"+gitDir)
			os.system("git --no-pager log --name-status --date=iso --reverse> ../seng371/input/"+gitDir+"-log.txt")

def parse():
	#Parse dem logs
	print "=====Parse the logs and look for Refactors====="
	for name in os.listdir("./input"):
		if name.endswith(".txt"):
			os.system("echo "+ name)
			inputfile = open("./input/"+name, 'r')
			out = name.replace("log", "out")
			outputfile = open("./output/"+out, 'w')
			lines = inputfile.readlines()
			added[x] = 0 
			delete = 0 
			modify = 0 
			diff = 0
			
			commit = ""
			date = ""
			comment = ""

			for line in lines:

				if line.startswith("A	"):
					added[x] = added[x] + 1 
				elif line.startswith("D	"):
					delete = delete + 1
				elif line.startswith("M	"):
					modify = modify + 1
				elif line.startswith("    "):
					comment = line[4:]
				elif line.startswith("commit"):
					commit = line[7:]
				elif line.startswith("Author:"):
					pass
				elif line.startswith("Date:"):
					tempdate = date
					date = line[8:-3] + "\n"
					if tempdate[:12] != date[:12]:
						lastdate = tempdate

				else:
					
					diff = abs(added[x] - delete)
					stats = [added[x],delete,modify, diff]
					if (added[x] == 0 and delete == 0):
						pass
		
						#outputfile.write("This commit was an update: " + str(stats)
					if (added[x] > 5 and delete > 5):
						outputfile.write("0-- This commit might be a refactor: Added[x] " + str(stats[0]) + ", Deleted " + str(stats[1]) + ", Modified " + str(stats[2]) + ", Diff " + str(stats[3])+ "\n")
						outputfile.write("1-- " + lastdate)
						outputfile.write("2-- " + date)
						outputfile.write("3-- " + comment)
						outputfile.write("\n\n")

					added[x] = 0
					delete = 0
					modify = 0
					diff = 0

def gource():
	print "=====Grab the refactors and them through gource====="
	for name in os.listdir("./output"):
		if name.endswith(".txt"):
			os.system("echo "+ name)
			inputfile = open("./output/"+name, 'r')
			lines = inputfile.readlines()

			gitDir = name[:-8]
			print gitDir
			os.chdir("../"+gitDir)

			for line in lines:
				if line.startswith("0-- "):
					pass
				elif line.startswith("1-- "):
					lastdate = line[4:]
				elif line.startswith("2-- "):
					date = line[4:]
				elif line.startswith("3-- "):
					comment = line[4:]
					command = 'gource --start-date "'+lastdate.strip()+'" --stop-date "'+date.strip()+'" -s 1 --key --title "' +gitDir + "     " + comment.strip() +'" --highlight-dirs'
					print command
					os.system(command)
			os.chdir(sys.path[0])

def graph():
		#Parse dem logs
	print "=====Parse the logs Graph====="
	for name in os.listdir("./input"):
		if name.endswith(".txt"):
			os.system("echo "+ name)
			inputfile = open("./input/"+name, 'r')
			out = name.replace("log", "out")
			outputfile = open("./output/"+out, 'w')
			lines = inputfile.readlines()
			added[x] = 0 
			delete = 0 
			modify = 0 
			diff = 0
			alpha = 0
			
			commit = ""
			date = ""
			comment = ""

			for line in lines:

				if line.startswith("A	"):
					added[x] = added[x] + 1 
				elif line.startswith("D	"):
					delete = delete + 1
				elif line.startswith("M	"):
					modify = modify + 1
				elif line.startswith("    "):
					comment = line[4:]
				elif line.startswith("commit"):
					commit = line[7:]
				elif line.startswith("Author:"):
					pass
				elif line.startswith("Date:"):
					tempdate = date
					date = line[8:-3] + "\n"
					

				else:
					
					diff = abs(added[x] - delete)
					stats = [added[x],delete,modify, diff]
					if (modify > 3):
						scale = modify
						color = "purple"
						alpha = .3
		
						#outputfile.write("This commit was an update: " + str(stats)
					if (added[x] > 1 and delete > 1):
						scale = added[x]+delete
						if (added[x]/delete) < 0.9:
							color = "red"
							alpha = .3
						elif (added[x]/delete) < 1.1:
							color = "green"
							alpha = .7
						else:
							color = "blue"
							alpha = .3

					if alpha != 0:
						date = dateutil.parser.parse(date)
						plt.scatter(date, scale, c=color, s=scale, label=color,
                alpha=alpha, edgecolors='none')
						

					added[x] = 0
					delete = 0
					modify = 0
					diff = 0
					alpha = 0


			plt.grid(True)
			plt.show()

def lines():
		#Parse dem logs
	print "=====Parse the logs Graph====="
	for name in os.listdir("./input"):
		if name.endswith(".txt"):
			os.system("echo "+ name)
			inputfile = open("./input/"+name, 'r')
			out = name.replace("log", "out")
			outputfile = open("./output/"+out, 'w')

			x = 0
			lines = inputfile.readlines()
			added= np.array([])
			delete = np.array([])
			modify = np.array([])
			z = np.array([])
			a = 0
			d = 0
			m = 0

			
			commit = ""
			date = ""
			comment = ""

			for line in lines:
				if line.startswith("A	"):
					a = a + 1 
				elif line.startswith("D	"):
					d = d + 1
				elif line.startswith("M	"):
					m =m + 1
				elif line.startswith("    "):
					comment = line[4:]
				elif line.startswith("commit"):
					commit = line[7:]
				elif line.startswith("Author:"):
					pass
				elif line.startswith("Date:"):
					tempdate = date
					date = line[8:-3] + "\n"
					

				else:

					if (a > 10) or (d > 10) or (m > 10):
						x = x + 1
						added = np.append(added, [a])
						delete = np.append(delete, [d])
						modify = np.append(modify, [m])
						z = np.append(z, [x])
					a = 0
					d = 0
					m = 0
			

			with plt.style.context('fivethirtyeight'):
				print added
				print x
				plt.plot(z, added)
				plt.plot(z, delete)
				plt.plot(z, modify)

			plt.show()
if __name__ == "__main__":
    main()