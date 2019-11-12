import nltk
import flask
import time
from flask import render_template, url_for, request, redirect, abort, json, flash
from Canary import ProcessInput, OutputFormat, DetectPeriodicSentences, ProcessOutput
import sys
from threading import Thread
from flask_cors import CORS

#Add the path to the perkeley parser to the system path
sys.path.insert(0, '../../../../perkeleyparser')

from BerkeleyParser import parser

#Define the relative paths for the berkeley parser
berkeleyPath = "../../../../berkeleyparser/berkeleyParser-1.7.jar"
grammarPath = "../../../../berkeleyparser/eng_sm6.gr"

#Define parameters for the berkeley parser, in this case telling it to tokenise the sentences
arguments = "-tokenize"

app = flask.Flask(__name__)

#Set the Access Control to *
CORS(app)

app.config["DEBUG"] = True

#Provide NLTK with a path to its installation
nltk.data.path.append(r"D:\Users\David\Documents\Work\University\Year 4\Honours\NLTK")

#Initialise the variables used to cache the parser and track it's status
parserIsTerminated = True
parserTool = None

def reloadParser():
    #Check if the parser has terminated, if so cache it again.
    global parserIsTerminated
    global parserTool
    global arguments

    if parserIsTerminated:
        print("Loading parser")
        parserTool = parser(berkeleyPath, grammarPath, arguments)

    parserIsTerminated = False
    
    print("Parser loaded.")

#Cache the parser using a thread after server load, allows server to load immediatley
parserReloadThread = Thread(target=reloadParser)
parserReloadThread.start()

def testAlgorithm():
    #Run tests
    allNewSentences = [] #This will hold all of the sentences from both batches
    output = ProcessInput.process("", "Periodic") #Load the periodic sentences ready for testing

    #Eveluate the periodic sentences
    output.sentences, periodicScore, numPeriodic = DetectPeriodicSentences.detectPeriodic(output.sentences, debug, argument, "Periodic", parserTool) #We don't know the nature of the sentences
    
    #Append the newly marked sentences to the allNewSentences array
    for sentence in output.sentences:
        sentence.knownType = "Periodic"
        allNewSentences.append(sentence)


    output = ProcessInput.process(text, "NotPeriodic") #Load the non-periodic sentences ready for testing

    #Evaluate the non-periodic sentences
    output.sentences, notPeriodicScore, numPeriodic = DetectPeriodicSentences.detectPeriodic(output.sentences, debug, argument, "NotPeriodic", parserTool) #We don't know the nature of the sentences

    #Append the newly marked sentences to the allNewSentences array
    for sentence in output.sentences:
        sentence.knownType = "Not Periodic"
        allNewSentences.append(sentence)

    #Return all of the sentences from both runs into our output object, ready to be displayed
    return allNewSentences, periodicScore, notPeriodicScore, numPeriodic

#The entry point to the algorithm for the user interface and external sources using the URL as an API
@app.route('/', methods=['GET'])
def API():
    #Get parameters from the URL
    text = request.args['text']
    textType = request.args['textType']
    outputFormat = request.args['outputFormat']
    debug = request.args['debug']
    argument = request.args['argument']

    #Other variables
    start = time.time() #To measure runtime
    periodicScore = 0 #Num of periodic sentences correctly predicted
    notPeriodicScore = 0 #Num of non-periodic sentences correctly predicted

    #Variables to track parser
    #We need to make sure the parser is cached. If not, cache it.
    global parserIsTerminated
    global parserReloadThread
    global parserTool
    
    if not parserReloadThread.isAlive():
        #Use a separate thread for starting the parser to prevent the application itself hanging
        parserReloadThread = Thread(target=reloadParser)
        parserReloadThread.start()

    parserReloadThread.join()

    #Work out the text type
    if textType == "Auto":
        if len(text.split()) == 1 and 'http' in text:
            textType = "URL"
        elif text == 'test':
            textType = "Test"
        else:
            textType = "Text"

    #Load the appropriate page based on textType
    if textType == "Test":
        output.sentences, periodicScore, notPeriodicScore, numPeriodic = testAlgorithm()
    else:
        output = ProcessInput.process(text, textType) #Process the text into an output format

        #Process, evaluate and store the sentences, score and number of periodic sentences detected
        output.sentences, score, numPeriodic = DetectPeriodicSentences.detectPeriodic(output.sentences, debug, argument, "Unknown", parserTool) #We don't know the nature of the sentences
    
    if numPeriodic > 1 or numPeriodic == 0:
        plural = "s"
    else:
        plural = ""
    
    #Terminate the parser, will need to be loaded again if needed.
    parserTool.terminate()
    parserIsTerminated = True

    #Set the output sentence for the summary page.
    output.numPeriodic = str(numPeriodic) + " periodic sentence" + plural + " detected."

    #End the timer and display the run time in the console
    end = time.time()
    print("Run time: " + str(end - start) + " seconds")
    
    #Output according to the outputFormat
    if outputFormat == 'html':
        #Load either the main page or the test page, depending on textType
        if textType == "Test":
            return render_template('test.html', output=output, periodicScore=periodicScore, notPeriodicScore=notPeriodicScore, debug=debug, runtime=str(round(end - start)))
        else:
            return render_template('render.html', output=output, debug=debug, textType=textType, argument=argument, runtime=str(round(end - start)))
    elif outputFormat == 'sadface':
        return ProcessOutput.renderSADFace(output)
    elif outputFormat == 'json':
        return ProcessOutput.renderJSON(output)
    elif outputFormat == 'pickle':
        return ProcessOutput.renderPickle(output)
    else:
        #Unrecognised output format, show appropriate error page
        return render_template('error/Format.html', outputFormat=outputFormat)
    return None

#Home page, loads a form that the user can edit to set parameters.
#GET returns the page template to the user and asks for their input
#POST sends the user's input to the server
@app.route('/home', methods=['POST','GET'])
def Home():
    if request.method == 'POST':
        #Take user's input and process using the API
        print(request.form)
        text = request.form['text']
        textType = request.form['textType']
        debug = request.form['debug']
        argument = request.form['argument']
        outputFormat = request.form['outputFormat']

        return redirect(url_for('.API', text=text, textType=textType, debug=debug, argument=argument, outputFormat=outputFormat))
    else:
        #Load the home page to get user input
        #We need to make sure the parser is cached. If not, cache it.
        global parserIsTerminated
        global parserReloadThread

        if not parserReloadThread.isAlive():
            parserReloadThread = Thread(target=reloadParser)
            parserReloadThread.start()
        return render_template('home.html')
        
#Render page, renders HTML to show the algorithm's output, such as a sentence breakdown showing which are periodic
@app.route('/render', methods=['GET'])
def Render():
    output = request.args['output']
    debug = request.args['debug']
    runtime = request.args['runtime']
    textType = request.args['textType']
    return render_template('render.html', output=output, debug=debug, runtime=runtime)

#Test page, shows test results
@app.route('/test', methods=['GET'])
def Test():
    output = request.args['output']
    debug = request.args['debug']
    runtime = request.args['runtime']
    return render_template('test.html', output=output, debug=debug, runtime=runtime)

#Error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('error/500.html'), 500

#Run the application
app.run()
