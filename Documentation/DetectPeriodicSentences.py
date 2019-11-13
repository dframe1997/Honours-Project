#Functions to detect periodic sentences
from Canary import SentenceFormat, helperFunctions
import nltk
import time
from nltk.tokenize import sent_tokenize
from nltk.tree import ParentedTree
import sys

#Add the path to the perkeley parser to the system path
sys.path.insert(0, '../../../../perkeleyparser')

from BerkeleyParser import parser

nltk.data.path.append(r"D:\Users\David\Documents\Work\University\Year 4\Honours\NLTK")

#Define the relative paths for the berkeley parser
berkeleyPath = "../../../../berkeleyparser/berkeleyParser-1.7.jar"
grammarPath = "../../../../berkeleyparser/eng_sm6.gr"

#Depth to search for subordinate conjunctions
subordinateConjunctionSearchDepth = 3 #2(60%) #3(70%) #4(57.81%) #5(51.39%) #7(24.8%)

#Check the first X words for the "IN" tag, indicating a subordinate clause and by extension a periodic sentence
def startingWords(sentence, debug):
    for index in range(subordinateConjunctionSearchDepth):
        if len(sentence.tagged) > index:
            if sentence.tagged[index][1] == "IN": #IN represents prepositions or 'subordinating conjunctions' which are often found at the start of a subordinate clause and therefore a periodic sentence
                return True
    return False       

#Check the sentence structure for signs of a subordinate clause
def treeStructure(sentence, debug, parserTool):
    #Based on characterizing stylistic elements

    #Parse the sentence and get it into a nltk tree format
    treeStringWBrackets = parserTool.parse(sentence.text)
    treeString = treeStringWBrackets[1:len(treeStringWBrackets)-1]
    sentence.entities = treeString

    #Turn the string generated by the parser into a tree object
    tree = ParentedTree.fromstring(treeString) 

    for subtree in tree.subtrees():     
        if subtree.parent() == tree:
            print(subtree.label())
             #tree height is the number of subtrees under it, so the top few layers will have the greatest height #Possibly dynamic based on length of sentence?
            if subtree.label() != "VP": #Some periodic sentences break this rule, fix to improve accuracy
                if any(x.label() == "S" for x in subtree.subtrees()) or any(x.label() == "SBAR" for x in subtree.subtrees()):
                    return True           
            #else:
            #if any(x.label() == "S" for x in subtree.subtrees()) or any(x.label() == "SBAR" for x in subtree.subtrees()):
                #return Loose
                # ONLY IMPLEMENT IF NEED TO DETECT LOOSE SENTENCES
    return False
    
#Detect periodic sentences using the algorithms above
def detectPeriodic(sentences, debug, checkArgument, natureOfSentences, parserTool):
    #Variables
    score = 0 #Only used in test mode
    numPeriodic = 0
    startingWordImpliesPeriodic = False
    treeStructureImpliesPeriodic = False
    
    #Loop through each sentence
    for sentence in sentences:
        #By default, we assume that the sentence is not periodic
        startingWordImpliesPeriodic = False
        treeStructureImpliesPeriodic = False

        if debug == "True":
            print(sentence.text)
            print(sentence.tokens)
            print(sentence.tagged)
            print(sentence.entities)
        #sentence.entities.draw() #This will draw the sentence tree, not used in the final build but useful for debugging
        
        #Run the starting words algorithm
        if startingWords(sentence, debug):
            startingWordImpliesPeriodic = True

        #Run the treeStructure algorithm
        if treeStructure(sentence, debug, parserTool):
            treeStructureImpliesPeriodic = True

        #If either imply a periodic sentence, label the sentence as such (or not)
        if startingWordImpliesPeriodic or treeStructureImpliesPeriodic:
            sentence.periodic = True
            numPeriodic += 1
            #If the sentence is in fact periodic (applies only to test mode) add a point to the score
            if natureOfSentences == "Periodic":
                score += 1
            print("'" + sentence.text + "'" + " is a periodic sentence.")
        else:
            sentence.periodic = False
            #If the sentence is in fact non-periodic (applies only to test mode) add a point to the score
            if natureOfSentences == "NotPeriodic":
                score += 1
            print("'" + sentence.text + "'" + " is not a periodic sentence.")
        
        #If we want to check for arguments, run the appropriate algorithm (Placeholder)
        if checkArgument and startingWordImpliesPeriodic and treeStructureImpliesPeriodic:
            sentence.argument = True

    #Assuming there is at least one sentence, calculate the score as a %
    if sentences.__len__() > 0: 
        score = (score/sentences.__len__())*100
    else:
        score = "N/A"
    
    return sentences, score, numPeriodic
