# Author: Paul Hamilton
# Project: Quizbowl Question Analysis
# Task: Frequency List
# Umich Unique Name: phamilt
# ----Subject: Fine Arts

import json
import csv
import re

#########################################################################################################
# INPUTS: A filename 																				  	#
# OUTPUTS: A dictionary 																			  	#
# PURPOSE: Create a dictionary where each key is a unique answer line and each value is a list of the 	#
#	questions with that answer line 																	#
#########################################################################################################

def create_question_dictionary(filename, categoryShort):

	fileObject = open(filename, 'rU')

	# Create a list from the JSON file where each element is a list containing a question, its answer line, and its difficulty
	questionAnswerList = []
	for pair in fileObject:
		questionAnswerList.append(json.loads(pair))

	# Create a dictionary where each key is a unique answer line and each value is a list of questions with that answer line
	questionAnswerDict = {}
	for pair in questionAnswerList:
		question = pair[0].encode('utf8')
		answerLine = pair[1].encode('utf8')
		difficulty = pair[2].encode('utf8')
		if answerLine not in questionAnswerDict.keys():
			questionAnswerDict[answerLine] = [[difficulty, question]]
		else:
			questionAnswerDict[answerLine].append([difficulty, question])

	# Output the dictionary as JSON to a text file
	outputFile = categoryShort + '_q_answ_dict_JSON.txt'
	outputFileObject = open(outputFile, 'w')
	questionAnswerDictJSON = json.dumps(questionAnswerDict)
	outputFileObject.write(questionAnswerDictJSON)
	outputFileObject.close()

	return questionAnswerDict

#########################################################################################################
# INPUTS: A dictionary containing answer lines and questions; a filename; a difficulty level	 		#
# OUTPUTS: A CSV file 																					#
# PURPOSE: Create a frequency list based on the question data stored in the questionAnswerDict 			#
#	dictionary 																							#
#########################################################################################################

def create_frequency_list(questionAnswerDict, outputFilename, difficultyCondition):

	frequencyList = []

	# Use dictionary to create a frequency list of unique answer lines and their number of occurances
	for answerLine in questionAnswerDict:
		questions = questionAnswerDict[answerLine]
		questionCount = 0
		for question in questions:
			difficulty = question[0]
			text = question[1]
			if re.match(difficultyCondition, difficulty) is not None:	# Only add a question to the frequency list if it is of the specified difficulty
				questionCount += 1
		frequencyList.append((answerLine, int(questionCount)))

	# Output the frequency to a csv file
	frequencyList = sorted(frequencyList, key = lambda pair: pair[1], reverse=True)
	frequencyListOutput = open(outputFilename, 'wb')
	csvWriter = csv.writer(frequencyListOutput)
	csvWriter.writerows(frequencyList)

#####################################################################################################################################################

def main():

	categoryShort = raw_input("Enter categoryShort (fa|lit|hist|sci|myth|ps|rel|geo): ")
	while not (categoryShort == "fa" or categoryShort == "lit" or categoryShort == "hist" or categoryShort == "sci" \
		or categoryShort=="myth" or categoryShort=="ps" or categoryShort =="rel" or categoryShort=="geo"):
		print "Invalid input"
		categoryShort = raw_input("Enter categoryShort (fa|lit|hist|sci|myth|ps|rel|geo): ")

	# Read in question data from the JSON file and create a dictionary
	question_data_JSON = categoryShort + '_q_answ_difficulties_JSON.txt'
	questionAnswerDict = create_question_dictionary(question_data_JSON, categoryShort)


	easyTournamentCondition = re.compile(r'E')
	easyTournamentFile = categoryShort + '_frequency_list_easy.csv'
	mediumTournamentCondition = re.compile(r'M')
	mediumTournamentFile = categoryShort + '_frequency_list_medium.csv'
	hardTournamentCondition = re.compile(r'H')
	hardTournamentFile = categoryShort + '_frequency_list_hard.csv'
	anyTournamentCondition = re.compile(r'[EMH]')
	anyTournamentFile = categoryShort + '_frequency_list_total.csv'

	# Create frequency lists for easy tournaments, medium-difficulty tournaments, hard tournaments, and all tournaments
	create_frequency_list(questionAnswerDict, easyTournamentFile, easyTournamentCondition)
	create_frequency_list(questionAnswerDict, mediumTournamentFile, mediumTournamentCondition)
	create_frequency_list(questionAnswerDict, hardTournamentFile, hardTournamentCondition)
	create_frequency_list(questionAnswerDict, anyTournamentFile, anyTournamentCondition)

if __name__ == "__main__":
    main()