from newspaper import Article
import nltk
import flask
import os
from nltk.corpus import treebank
from nltk.tokenize import sent_tokenize
from nltk.corpus.reader import ChunkedCorpusReader
from nltk.tree import Tree
from flask import render_template, url_for, request, redirect, abort, json, flash
import sys

sys.path.insert(0, '../../../perkeleyparser')

from BerkeleyParser import parser

app = flask.Flask(__name__)
app.config["DEBUG"] = True

nltk.data.path.append(r"D:\Users\David\Documents\Work\University\Year 4\Honours\NLTK")

berkeleyPath = "../../../berkeleyparser/berkeleyParser-1.7.jar"
grammarPath = "../../../berkeleyparser/eng_sm6.gr"

treeSearchDepth = 1
class SentenceObject:
    text = ""
    tokens = []
    tagged = []
    entities = []
    periodic = False

def cls():
    n = 0
    while n < 100:
        print("\n")
        n = n + 1

def filter(tree):
        child_nodes = [child.label() for child in tree if isinstance(child, nltk.Tree)]
        return  (tree.label() == 'VP') and ('S' in child_nodes)

def openFile(fileLocation):
    inputFile = open(fileLocation, "r")
    inputContent = ""
    if inputFile.mode == 'r':
        inputContent = inputFile.read()
    
    if(debug): 
        print("File opened successfully. Attempting to detect periodic sentences...")
    
    if inputContent == "":
        print("ERROR: No Text found. Please add text to the file.")
    
    return inputContent

def splitSentences(text):
    #Splitting the article into sentences
    sentenceList = []
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentenceObject = SentenceObject()

        sentenceObject.text = sentence

        sentenceObject.tokens = nltk.word_tokenize(sentence)

        sentenceObject.tagged = nltk.pos_tag(sentenceObject.tokens)
        #output += tagged[0:6]

        sentenceObject.entities = nltk.chunk.ne_chunk(sentenceObject.tagged)

        #tree = [subtree for tree in treebank.parsed_sents() for subtree in tree.subtrees(filter)]
        #print tree

        #from nltk.corpus import treebank
        #t = treebank.parsed_sents('wsj_0001.mrg')[0]
        #entities.draw()
        sentenceList.append(sentenceObject)
    return sentenceList

def startingWords(sentence, debug):
    startingFile = open("Dataset/Keywords/StartingWords.txt", "r")
    startingWords = []
    if startingFile.mode == 'r':
        startingWords = startingFile.read()
        if(debug == True): print("Attempting to match keywords...")
        for word in startingWords.split(","):
            if sentence.text.startswith(word):
                return True
        return False          

def treeShape(sentence, debug):
    if sentence.entities.height() < 3:
        print(sentence.entities)
        print(sentence.entities.height())
        print(len(sentence.entities.leaves()))
        return True
    else:
        return False

def treeStructure(sentence, debug):
    #Based on characterizing stylistic elements
    p = parser(berkeleyPath, grammarPath)
    treeString = p.parse(sentence.text)
    p.terminate()
    tree = Tree.fromstring(treeString)
    #topOfTree = tree[0:treeSearchDepth] #It's not a string - need a new way to get the top layers of tree
    topOfTree = tree
    for node in topOfTree:
        h = node.height()
        if h <= treeSearchDepth:
            if node.label() != "VP":
                if any(x.label() == "S" for x in topOfTree) or any(x.label() == "SBAR" for x in topOfTree):
                    return True
            else:
                if any(x.label() == "S" for x in topOfTree) or any(x.label() == "SBAR" for x in topOfTree):
                    return False
    return False

def detectPeriodic(text, debug, natureOfSentences):
    sentences = splitSentences(text)
    score = 0
    for sentence in sentences:
        if(debug == True):
            print(sentence.text)
            print(sentence.tokens)
            print(sentence.tagged)
            print(sentence.entities)
        #sentence.entities.draw()
        if startingWords(sentence, debug) or treeStructure(sentence, debug):
            sentence.periodic = True
            if natureOfSentences == "Periodic":
                score += 1
            print("'" + sentence.text + "'" + " is a periodic sentence.")
        else:
            sentence.periodic = False
            if natureOfSentences == "NotPeriodic":
                score += 1
            print("'" + sentence.text + "'" + " is not a periodic sentence.")

    score = (score/sentences.__len__())*100
    return score

#Main program
#Options
import time
start = time.time()

testModeInput = input("Run test mode? (Default: N)")
testMode = False

if "y" in testModeInput.lower():
    testMode = True
else:
    testMode = False

debugInput = input("Show debug messages? (Default: N)")
debug = False

if "y" in debugInput.lower():
    debug = True
else:
    debug = False

if testMode:
    inputContent = openFile("Dataset/Periodic.txt")
    cls()
    score = detectPeriodic(inputContent, debug, "Periodic") #The first test will check the periodic sentences
    print(str(score) + "% of periodic sentences correctly identified.")
    print("_________________________________________________")
    inputContent = openFile("Dataset/NotPeriodic.txt")
    score = detectPeriodic(inputContent, debug, "NotPeriodic") #The first test will check the periodic sentences
    print(str(score) + "% of non-periodic sentences correctly identified.")
else:
    fileLocation = input("Please type the filepath for the text you want to analyse. To use the default, simply press enter.")
    if fileLocation == "":
        fileLocation = "Input.txt"
    inputContent = openFile(fileLocation)
    cls()
    detectPeriodic(inputContent, debug, "Unknown") #We don't know the nature of the sentences

end = time.time()
print("Run time: " + (end - start))
input("Press Enter to continue...")


