import nltk
import flask
import time
from flask import render_template, url_for, request, redirect, abort, json, flash
from Canary import ProcessInput, OutputFormat, periodic, ProcessOutput
import sys
from threading import Thread

sys.path.insert(0, '../../../../perkeleyparser')

from BerkeleyParser import parser

berkeleyPath = "../../../../berkeleyparser/berkeleyParser-1.7.jar"
grammarPath = "../../../../berkeleyparser/eng_sm6.gr"
arguments = "-tokenize"

app = flask.Flask(__name__)
app.config["DEBUG"] = True

nltk.data.path.append(r"D:\Users\David\Documents\Work\University\Year 4\Honours\NLTK")

parserIsTerminated = True

parserTool = None

fromHomePage = False

#file = request.files['file']
#f = secure_filename(file.filename)
#text=f.read()

def reloadParser():
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

@app.route('/', methods=['GET'])
def API():
    text = request.args['text']
    textType = request.args['textType']
    outputFormat = request.args['outputFormat']
    debug = request.args['debug']
    argument = request.args['argument']
    start = time.time()
    periodicScore = 0
    notPeriodicScore = 0
    global parserIsTerminated
    global parserReloadThread
    global parserTool
    
    if not parserReloadThread.isAlive():
        parserReloadThread = Thread(target=reloadParser)
        parserReloadThread.start()

    parserReloadThread.join()

    fromHomePage = False

    if textType == "Test":
        allNewSentences = []
        output = ProcessInput.process(text, "Periodic") 
        output.sentences, periodicScore, numPeriodic = periodic.detectPeriodic(output.sentences, debug, argument, "Periodic", parserTool) #We don't know the nature of the sentences
        
        for sentence in output.sentences:
            sentence.knownType = "Periodic"
            allNewSentences.append(sentence)

        output = ProcessInput.process(text, "NotPeriodic") 
        output.sentences, notPeriodicScore, numPeriodic = periodic.detectPeriodic(output.sentences, debug, argument, "NotPeriodic", parserTool) #We don't know the nature of the sentences
    
        for sentence in output.sentences:
            sentence.knownType = "Not Periodic"
            allNewSentences.append(sentence)

        output.sentences = allNewSentences
    else:
        output = ProcessInput.process(text, textType)   
        output.sentences, score, numPeriodic = periodic.detectPeriodic(output.sentences, debug, argument, "Unknown", parserTool) #We don't know the nature of the sentences
    
    if numPeriodic > 1 or numPeriodic == 0:
        plural = "s"
    else:
        plural = ""
    
    parserTool.terminate()
    parserIsTerminated = True

    output.numPeriodic = str(numPeriodic) + " periodic sentence" + plural + " detected."
    end = time.time()
    print("Run time: " + str(end - start) + " seconds")
    
    if outputFormat == 'html':
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
        return '<h2>Sorry, "' + outputFormat + '" is not a supported output format. Please specify "html", "json", "pickle" or "sadface" as the output format instead.<h2>'
    return None

@app.route('/home', methods=['POST','GET'])
def Home():
    if request.method == 'POST':
        print(request.form)
        text = request.form['text']
        textType = request.form['textType']
        debug = request.form['debug']
        argument = request.form['argument']
        outputFormat = request.form['outputFormat']

        return redirect(url_for('.API', text=text, textType=textType, debug=debug, argument=argument, outputFormat=outputFormat))
    else:
        global parserIsTerminated
        global parserReloadThread

        if not parserReloadThread.isAlive():
            parserReloadThread = Thread(target=reloadParser)
            parserReloadThread.start()
        return render_template('home.html')
        

@app.route('/render', methods=['GET'])
def Render():
    output = request.args['output']
    debug = request.args['debug']
    runtime = request.args['runtime']
    textType = request.args['textType']
    return render_template('render.html', output=output, debug=debug, runtime=runtime)

@app.route('/test', methods=['GET'])
def Test():
    output = request.args['output']
    debug = request.args['debug']
    runtime = request.args['runtime']
    return render_template('test.html', output=output, debug=debug, runtime=runtime)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('error/500.html'), 500
app.run()
