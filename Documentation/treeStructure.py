#Functions to detect periodic sentences
from Canary import SentenceFormat, helperFunctions
import nltk
import time
from nltk.tokenize import sent_tokenize
from nltk.tree import ParentedTree
import sys

sys.path.insert(0, '../../../../perkeleyparser')

from BerkeleyParser import parser

nltk.data.path.append(r"D:\Users\David\Documents\Work\University\Year 4\Honours\NLTK")

berkeleyPath = "../../../../berkeleyparser/berkeleyParser-1.7.jar"
grammarPath = "../../../../berkeleyparser/eng_sm6.gr"

subordinatingConjunctionSearchDepth = 3 #2(60%) #3(70%) #4(57.81%) #5(51.39%) #7(24.8%)
depthIncreaseThreshold = 10

def startingWords(sentence, debug):
    for index in range(subordinatingConjunctionSearchDepth):
        if len(sentence.tagged) > index:
            if sentence.tagged[index][1] == "IN":# or sentence.tagged[index][1] == "WDT" or sentence.tagged[index][1] == "WP" or sentence.tagged[index][1] == "WP$" or sentence.tagged[index][1] == "WRB": #IN represents prepositions or 'subordinating conjunctions' which are often found at the start of a subordinate clause and therefore a periodic sentence
                return True
    return False       

def treeStructure(sentence, debug, parserTool):
    #Based on characterizing stylistic elements
    #while parserTool == None:
        #time.sleep(1)
        #print("Waiting for parser to load before creating tree.")
    treeStringWBrackets = parserTool.parse(sentence.text)
    treeString = treeStringWBrackets[1:len(treeStringWBrackets)-1]
    #parserTool.terminate() #End the parser process to save memory
    sentence.entities = treeString
    tree = ParentedTree.fromstring(treeString) #Turn the string generated by the parser into a tree object

    #topOfTree = tree[0:treeSearchDepth] #It's not a string - need a new way to get the top layers of tree
    #tree.draw()
    #treeSize = sum(1 for x in tree.subtrees())
    index = 0

    for subtree in tree.subtrees():     
        if subtree.parent() == tree: #MAY BE INCORRECT
            print(subtree.label())
             #tree height is the number of subtrees under it, so the top few layers will have the greatest height #Possibly dynamic based on length of sentence?
            if subtree.label() != "VP": #Some periodic sentences break this rule, fix to improve accuracy
                if any(x.label() == "S" for x in subtree.subtrees()) or any(x.label() == "SBAR" for x in subtree.subtrees()):
                    return True
                #elif subtree.label() == "S" or subtree.label() == "SBAR":
                    #return True
            
            #else:
            #if any(x.label() == "S" for x in subtree.subtrees()) or any(x.label() == "SBAR" for x in subtree.subtrees()):
                #return Loose
                # ONLY IMPLEMENT IF NEED TO DETECT LOOSE SENTENCES
        index += 1
    return False
    

def detectPeriodic(sentences, debug, checkArgument, natureOfSentences, parserTool):
    score = 0
    numPeriodic = 0
    startingWordImpliesArgument = False
    treeStructureIsPeriodic = False
    
    for sentence in sentences:
        startingWordImpliesArgument = False
        treeStructureIsPeriodic = False
        if debug == "True":
            print(sentence.text)
            print(sentence.tokens)
            print(sentence.tagged)
            print(sentence.entities)
        #sentence.entities.draw()
        if startingWords(sentence, debug):
            startingWordImpliesArgument = True
            #if checkArgument:
                #if treeStructure(sentence, debug, parserTool):
                    #treeStructureIsPeriodic = True
        if treeStructure(sentence, debug, parserTool):
            treeStructureIsPeriodic = True

        if startingWordImpliesArgument or treeStructureIsPeriodic:
            sentence.periodic = True
            numPeriodic += 1
            if natureOfSentences == "Periodic":
                score += 1
            print("'" + sentence.text + "'" + " is a periodic sentence.")
        else:
            sentence.periodic = False
            if natureOfSentences == "NotPeriodic":
                score += 1
            print("'" + sentence.text + "'" + " is not a periodic sentence.")
        
        if checkArgument and startingWordImpliesArgument and treeStructureIsPeriodic:
            sentence.argument = True

    if sentences.__len__() > 0: 
        score = (score/sentences.__len__())*100
    else:
        score = "N/A"
    
    return sentences, score, numPeriodic
