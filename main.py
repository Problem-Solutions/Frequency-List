# Author: Paul Hamilton
# Project: Quizbowl Question Analysis
# ----Subject: Fine Arts

import json
import csv

#######################################################################################################################################
# INPUTS: A filename 																												  #
# OUTPUTS: A dictionary 																											  #
# PURPOSE: Create a dictionary where each key is a unique answer line and each value is a list of the questions with that answer line #
#######################################################################################################################################

def create_question_dictionary(filename):

	fileObject = open(filename, 'rU')

	questionAnswerList = []
	for pair in fileObject:
		questionAnswerList.append(json.loads(pair))

	questionAnswerDict = {}
	for pair in questionAnswerList:
		question = pair[0].encode('utf8')
		answerLine = pair[1].encode('utf8')
		difficulty = pair[2].encode('utf8')
		if answerLine not in questionAnswerDict.keys():
			questionAnswerDict[answerLine] = [difficulty, question]
		else:
			questionAnswerDict[answerLine].extend([question])

	return questionAnswerDict

###########################################################################################################
# INPUTS: A dictionary, a filename, a string															  #
# OUTPUTS: A CSV file 																					  #
# PURPOSE: Create a frequency list based on the question data stored in the questionAnswerDict dictionary #
###########################################################################################################

def create_frequency_list(questionAnswerDict, outputFilename, difficultyCondition):

	frequencyList = []
	for answerLine in questionAnswerDict:
		if questionAnswerDict[answerLine][0] == difficultyCondition:
			frequency = float(len(questionAnswerDict[answerLine]) - 1) / len(questionAnswerDict)
			frequencyList.append((answerLine, frequency))
	frequencyList = sorted(frequencyList, key = lambda pair: pair[1], reverse=True)
	frequencyListOutput = open(outputFilename, 'wb')
	csvWriter = csv.writer(frequencyListOutput)
	csvWriter.writerows(frequencyList)

#############################################################################################################################################

def main():

	# Read in question data from the JSON file and create a dictionary
	question_data_JSON = 'Question Answer Pairs with Difficulties JSON.txt'
	questionAnswerDict = create_question_dictionary(question_data_JSON)

	easyTournamentCondition = 'E'
	easyTournamentFile = 'Frequency List Easy.csv'
	mediumTournamentCondition = 'M'
	mediumTournamentFile = 'Frequency List Medium.csv'
	hardTournamentCondition = 'H'
	hardTournamentFile = 'Frequency List Hard.csv'
	anyTournamentCondition = r'.'
	anyTournamentFile = 'Frequency List Total.csv'

	# Create frequency lists for easy tournaments, medium-difficulty tournaments, hard tournaments, and all tournaments
	create_frequency_list(questionAnswerDict, easyTournamentFile, easyTournamentCondition)
	create_frequency_list(questionAnswerDict, mediumTournamentFile, mediumTournamentCondition)
	create_frequency_list(questionAnswerDict, hardTournamentFile, hardTournamentCondition)
	create_frequency_list(questionAnswerDict, anyTournamentFile, anyTournamentCondition)

if __name__ == "__main__":
    main()