# Quizbowl-Frequency-List

This program creates a frequency list of fine arts answer lines, stratified by tournament difficulty. It could easy be applied to other disciplines, but 
  the quality of the results will be lower for disciplines with a greater variability of answer lines. 

The goal of this program is to take a file of fine arts quizbowl questions and create four frequency lists: one for easy 
  tournaments, one for medium-difficulty tournaments, one for hard tournaments, and one for an aggregate of all tournaments. The questions were downloaded from 
  quinterest.com.
  
### For those unframiliar with quizbowl

Quizbowl is a competitive activity that tests players' knowledge of a variety of academic subjects. It is practiced at the middle school, high school, and collegiate
  levels. In a traditional quizbowl match, two teams consisting of four players each face off on a series of twenty "tossups" (the lingo for question), each of which 
  is accomanied by a series of three bonus questions that can be answered only by the team that answers the tossup correctly. There are no strict rules for the subject
  of the twenty tossups, but most tournaments follow a distribution similar to this: science (4 tossups), literature (4 tossups), history (4 tossups), fine arts
  (3 tossups), mythology/philosophy/religion (3 tossups), geography/current events (1 tossup), and trash (1 tossup). Within these subjects, question writers are allowed
  to write on anything they want. However, there is an informal canon of material that question writers tend to stick to. The optimal studying strategy is therefore 
  to get a sense of what answer lines have come up in the past, as these answer lines will most likely come up again. As one would imagine, this makes a frequency list
  that orders answer lines based on their frequency of appearance extremely useful. It is the goal of this project to create such a frequency list for fine arts. Fine 
  arts was chosen both because it is the subject area I know the most about and because the answer lines tend to be more standardized than other disciplines, such as 
  science. 
  
  Before moving on, it is a good idea to get acclimated with the format of quizbowl tossups. Take the following question from New Trier's 2014 Scobol Solo tournament:
  
      QUESTION: Among this composer's five cello sonatas is the Sonata for Cello and Piano in A major he dedicated to Ignaz Gleichenstein. One of his rondos is nicknamed 
      "Rage Over a Lost Penny". He named one of his pieces Sonata quasi una fantasia, but it was given a more famous nickname by Ludwig Rellstab based on viewings of 
      Lake Lucerne. His fifth and sixth symphonies premiered the same night, and his fifth has a famous short-short-short-long motif. His third symphony was originally 
      dedicated to Napoleon. Name this German composer of Eroica, "Für Elise", and the "Moonlight Sonata", who used Friedrich Schiller's "Ode to Joy" in his 9th symphony.

      ANSWER: Ludwig van Beethoven
      
   As you can see, most questions are multiple sentences long. A good quizbowl tossup will get more difficult as the question progresses, so that the clues used in the 
   first line are relatively difficult and the clues used in the last line are relatively easy. 
   
### Mechanics of the project
 
 The data used in this project was downloaded from quinterest.com, a searchable quizbowl database. The file "FA Questions Unprocessed.txt" contains a list of all of the
  fine arts questions collected on the site, for a total of around 7,500. From a high level, this project simply traverses through this list and creates a count for each
  unique answer line. Sorting this list in descending order provides a list of tossups based on frequency of occurance. 
  
 The most difficult part of accomplishing this is handling answer lines that refer to the same thing but are semantically different. For example, "Johann Sebastian Bach" 
  and "J.S. Bach" both refer to the 18th century German composer but are semantically different. Instead of trying to match these on my own, I pass each answer line to 
  the Wikipedia api. I then take the headline of the top-matched article from each search and use these instead of the actual answer lines from the questions. For example, 
  passing the two versions of Bach to Wikipedia directs to the Wikipedia page "Johann Sebastian Bach", so both versions are replaced with this and the matching problem 
  is eliminated. I am in essence hijacking Wikipedia's matching algorithm instead of writing my own. This process can be found in the file "wikipediaScript.py", which 
  outputs a JSON file ("Question Answer Pairs with Difficulties JSON"). The JSON file contains a list of lists, where each element in the list is of the following format:
      [Question, Answer Line (standardized), Difficulty]
    
 The next portion of the project ("main.py") reads in the data from the JSON file and uses it to create a dictionary. Each key of the dictionary is a unique answer line, 
  and each value is a list of the questions with that answer line and that question's difficulty. For example:
      key (unique answer line): value (list of questions and difficulties)
      'Johann Sebastian Bach': [["Among this composer's five cello sonatas is the Sonata for Cello and Piano in A major he dedicated to Ignaz Gleichenstein. One of his rondos
      is nicknamed "Rage Over a Lost Penny". He named one of his pieces Sonata quasi una fantasia, but it was given a more famous nickname by Ludwig Rellstab based on viewings
      of Lake Lucerne. His fifth and sixth symphonies premiered the same night, and his fifth has a famous short-short-short-long motif. His third symphony was originally 
      dedicated to Napoleon. Name this German composer of Eroica, "Für Elise", and the "Moonlight Sonata", who used Friedrich Schiller's "Ode to Joy" in his 9th symphony.", "M"],
      ["In one of this composer's pieces, Pales sings the aria, "Sheep May Safely Graze." He used trumpets and five voices to conclude the "Symbolum Nicenum" section of another
      work. This composer of Hunting Cantata and Mass in B minor based another of his works on a theme given by Frederick the Great. He wrote (*) 24 preludes and fugues in 
      every key in a work named after a tuning system. This composer of The Musical Offering produced a work dedicated to Christian Ludwig that was comprised of a set of six 
      musical pieces. For ten points, name this German composer of The Well-Tempered Clavier and Brandenburg Concertos.", "E"]]
  
  The script then creates a list, where each element of the list is a tuple containing an answer line and the number of times that answer line appeared. For example:
      [('J.S. Bach', 10), ('Picasso', 7), ... ]
  This list can then be sorted in descending order and outputted to a csv. The final frequency lists are excel files titles "Frequency List Total", "Frequency List Easy", etc. 
  
### Final Note
  It wasn't actually necessary to separate the project into two scripts and output the dictionary to a JSON file. However, I did this because I plan to use this
  data in other projects. My next project will be to use some natural language processing techniques on the questions themselves. 
  
