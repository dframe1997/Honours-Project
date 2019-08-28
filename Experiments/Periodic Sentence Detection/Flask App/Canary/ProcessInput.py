from newspaper import Article
from Canary import SentenceFormat, OutputFormat
import nltk
from nltk.tokenize import sent_tokenize
from string import printable

nltk.data.path.append(r"D:\Users\David\Documents\Work\University\Year 4\Honours\NLTK")

def openFile(fileLocation, debug):
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
    sentenceObjectList = []
    sentenceTextList = sent_tokenize(text)
    if not sentenceTextList:
        sentenceTextList = [text]
        print("Saved the day")
    for sentenceText in sentenceTextList:
        sentenceText = ''.join(char for char in sentenceText if char in printable) #Remove hidden characters
        sentenceText = sentenceText.replace('\n', ' ').replace('\r', '')

        tokens = nltk.word_tokenize(sentenceText)

        tagged = nltk.pos_tag(tokens)

        tree = None

        newSentence = SentenceFormat.SentenceObject(sentenceText, tokens, tagged, tree)
        sentenceObjectList.append(newSentence)
    return sentenceObjectList

def processURL(url):
    article = Article(url)
    article.download()
    article.parse()   
    article.nlp()
    sentences = splitSentences(article.text)

    output = OutputFormat.Output(url, article.title, article.authors, article.publish_date, article.top_image, article.movies, article.text, article.keywords, article.summary, 0, sentences)
    return output

def process(text, textType):
    if textType == "URL":
        output = processURL(text)
        return output
    elif textType == "File":
        if text == "":
            text = "Input.txt"
        sentencesText = openFile(text)
        sentences = splitSentences(sentencesText)
        output = OutputFormat.Output(text, "Input from file", "No author specified", "Publish date unknown", "top_image", "movies", sentencesText, "No keywords found", "", 0, sentences)
        return output
    elif textType == "Periodic":
        sentencesText = openFile("D:/Users/David/Documents/Work/University/Year 4/Honours/Honours-Project/Experiments/Periodic Sentence Detection/Dataset/Periodic.txt", True)
        sentences = splitSentences(sentencesText)
        output = OutputFormat.Output(text, "Input from file", "No author specified", "Publish date unknown", "top_image", "movies", sentencesText, "No keywords found", "", 0, sentences)
        return output
    elif textType == "NotPeriodic":
        sentencesText = openFile("D:/Users/David/Documents/Work/University/Year 4/Honours/Honours-Project/Experiments/Periodic Sentence Detection/Dataset/NotPeriodic.txt", True)
        sentences = splitSentences(sentencesText)
        output = OutputFormat.Output(text, "Input from file", "No author specified", "Publish date unknown", "top_image", "movies", sentencesText, "No keywords found", "", 0, sentences)
        return output
    else:
        sentences = splitSentences(text)
        output = OutputFormat.Output(text, "Input from webpage", "No author specified", "Publish date unknown", "top_image", "movies", text, "No keywords found", "", 0, sentences)
        return output