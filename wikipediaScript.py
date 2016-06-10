# Author: Paul Hamilton
# Project: Quizbowl Question Analysis
# Task: Frequency List
# Umich Unique Name: phamilt
# ----Subject: Fine Arts

import wikipedia
import re
import json
import itertools
import sys

#############################################################################
# INPUTS: A filename														#
# OUTPUTS: A dictionary														#
# PURPOSE: Create dictionary that relates each tournament to its difficulty #
#############################################################################

def read_in_tournament_difficulties(filename):

	# Create a dictionary where each key is a tournament's name and each value is the tournament's difficulty
	# Easy == "E", Medium == "M", Hard == "H"
	tournamentDifficultyDict = {}
	fileObject = open(filename)

	for line in fileObject:
		tournamentAndDifficulty = line.split('\t')
		print tournamentAndDifficulty	
		tournamentName = tournamentAndDifficulty[0]
		difficulty = tournamentAndDifficulty[1]
		tournamentDifficultyDict[tournamentName] = difficulty
	return tournamentDifficultyDict
	fileObject.close()
##################################################################################
# INPUTS: A filename; a dictionary 												 #
# OUTPUTS: A list of lists 													     #
# PURPOSE: Creates a list of each tossup's answer line, question, and difficulty #
##################################################################################

def create_question_answer_pairs(filename, tournamentDifficultyDict):

	# Used to extract tournament name that the tossup is from 
	TOURNAMENT_RE = re.compile(r'Result:\s[0-9]{1,5}\s\|\s(.*?)\s\|')

	# Used to remove comments after answer line
	BRACKET_RE = re.compile(r'\[.*')
	PARANTHESES_RE = re.compile(r'\(.*')
	OR_RE = re.compile(r'\s[oO][rR]\s.*')

	questionData = []
	count = 1

	fileObject = open(filename)
	for line in fileObject:

		# Get the tounament difficulty for a tossup
		if (line[0:6] == 'Result'):
			tournament = re.findall(TOURNAMENT_RE, line)[0]
			difficulty = tournamentDifficultyDict[tournament]
			difficulty = difficulty.replace('\n', '')
			questionData.append(difficulty)

		# Get the question text of a tossup
		if (line[0:8] == 'Question'):
			question = line[10:]
			question = question.replace('\n', '')
			questionData.append(question)

		# Get the answer line of a tossup
		if (line[0:6] == 'ANSWER'):
			answerLine = line[8:]

			# Remove unnecessary comments surrounding the answer line
			answerLine = re.sub(BRACKET_RE, '', answerLine)
			answerLine = re.sub(PARANTHESES_RE, '', answerLine)
			answerLine = re.sub(OR_RE, '', answerLine)
			answerLine = answerLine.replace('\n', '')

			try:
				# Try passing the answer line to wikipedia in order to use its search matching algorithm
				wikipediaResult = wikipedia.search(answerLine)
				wikipediaResult = wikipediaResult[0]
				print wikipediaResult
				questionData.append(wikipediaResult)
			except:
				print answerLine
				questionData.append(answerLine)
			print count 
			count += 1

	fileObject.close()
	# Combine the difficulty, question, and answer line for each tossup into a list of lists
	iterableList = iter(questionData)
	questionAnswerPairs = zip(iterableList, iterableList, iterableList)

	return questionAnswerPairs

#############################################
# INPUTS: A filename, a list of lists		#
# OUTPUTS: None								#
# PURPOSE: Print tossup data to a JSON file #
#############################################

def output_data_to_JSON(filename, questionAnswerPairs):

	# Output the question answer pairs to a csv file
	outputObject = open(filename, 'w')

	for element in questionAnswerPairs:
		outputObject.write(json.dumps(element))
		outputObject.write('\n')

	outputObject.close()	

#####################################################################################################################################################

def main():

	categoryShort = raw_input("Enter categoryShort (fa|lit|hist|sci|myth|ps|rel|geo): ")
	while not (categoryShort == "fa" or categoryShort == "lit" or categoryShort == "hist" or categoryShort == "sci" \
		or categoryShort=="myth" or categoryShort=="ps" or categoryShort =="rel" or categoryShort=="geo"):
		print "Invalid input"
		categoryShort = raw_input("Enter categoryShort (fa|lit|hist|sci|myth|ps|rel|geo): ")
	"""categoryLong ={
		'fa'  : lambda: "Fine Arts",
		'lit' : lambda: "Literature",
		'hist': lambda: "History",
		'sci' : lambda: "Science",
		'myth': lambda: "Mythology",
		'ps'  : lambda: "Philosophy and Social Science",
		'rel' : lambda: "Religion",
		'geo' : lambda: "Geography"
	}[]
	"""
	# Create a dictionary where each key is a tournament name and each value is that tournament's difficulty ('E', 'M', or 'H')
	tournamentDifficultyFile = "tournament_difficulties.txt"
	tournamentDifficultyDict = read_in_tournament_difficulties(tournamentDifficultyFile)
	
	# Create a list of data (question, difficulty, answer line) for each tossup
	unprocessedQuestionsFile = "unprocessed_questions_" + categoryShort + ".txt"
	questionAnswerPairs = create_question_answer_pairs(unprocessedQuestionsFile, tournamentDifficultyDict)


	# Print the question data to a JSON file
	outputFile = categoryShort +'_q_answ_difficulties_JSON.txt'
	output_data_to_JSON(outputFile, questionAnswerPairs)

if __name__ == "__main__":
    main()