# Author: Paul Hamilton
# Project: Quizbowl Question Analysis
# ----Subject: Fine Arts

import wikipedia
import re
import json
import itertools

#############################################################################
# INPUTS: A filename														#
# OUTPUTS: A dictionary														#
# PURPOSE: Create dictionary that relates each tournament to its difficulty #
#############################################################################

def read_in_tournament_difficulties(filename):

	tournamentDifficultyDict = {}
	fileObject = open(filename)
	for line in fileObject:
		tournamentAndDifficulty = line.split('\t')
		tournamentName = tournamentAndDifficulty[0]
		difficulty = tournamentAndDifficulty[1]
		tournamentDifficultyDict[tournamentName] = difficulty
	return tournamentDifficultyDict

##################################################################################
# INPUTS: A filename, a dictionary 												 #
# OUTPUTS: A list of lists 													     #
# PURPOSE: Creates a list of each tossup's answer line, question, and difficulty #
##################################################################################

def create_question_answer_pairs(filename, tournamentDifficultyDict):

	# Used to extract tournament name tossup is from 
	TOURNAMENT_RE = re.compile(r'Result:\s[0-9]{1,4}\s\|\s(.*?)\s\|')
	# Removes comments after tossup
	BRACKET_RE = re.compile(r'\[.*')
	# Removes comments after tossup
	PARANTHESES_RE = re.compile(r'\(.*')
	# Removes comments after tossup
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
				questionData.append(wikipediaResult)
			except:
				questionData.append(answerLine)
			print count 
			count += 1

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

	outputObject = open(filename, 'w')
	for element in questionAnswerPairs:
		outputObject.write(json.dumps(element))
		outputObject.write('\n')
		print json.dumps(element)
	outputObject.close()	

###################################################################################################################################

def main():

	# Create a dictionary where each key is a tournament name and each value is that tournament's difficulty ('E', 'M', or 'H')
	tournamentDifficultyFile = 'List of Tournaments With Difficulties.txt'
	tournamentDifficultyDict = read_in_tournament_difficulties(tournamentDifficultyFile)

	# Create a list of data (question, difficulty, answer line) for each tossup
	unprocessedQuestionsFile = 'FA Questions Unprocessed.txt'
	questionAnswerPairs = create_question_answer_pairs(unprocessedQuestionsFile, tournamentDifficultyDict)

	# Print the question data to a JSON file
	outputFile = 'Question Answer Pairs with Difficulties JSON.txt'
	output_data_to_JSON(outputFile, questionAnswerPairs)
	

if __name__ == "__main__":
    main()