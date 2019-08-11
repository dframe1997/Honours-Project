import nltk
import flask
import time
from flask import render_template, url_for, request, redirect, abort, json, flash
from Canary import ProcessInput, OutputFormat, periodic, ProcessOutput

app = flask.Flask(__name__)
app.config["DEBUG"] = True

nltk.data.path.append(r"D:\Users\David\Documents\Work\University\Year 4\Honours\NLTK")

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

    if textType == "Test":
        allNewSentences = []
        output = ProcessInput.process(text, "Periodic") 
        output.sentences, periodicScore, numPeriodic = periodic.detectPeriodic(output.sentences, debug, argument, "Periodic") #We don't know the nature of the sentences
        
        for sentence in output.sentences:
            sentence.knownType = "Periodic"
            allNewSentences.append(sentence)

        output = ProcessInput.process(text, "NotPeriodic") 
        output.sentences, notPeriodicScore, numPeriodic = periodic.detectPeriodic(output.sentences, debug, argument, "NotPeriodic") #We don't know the nature of the sentences
    
        for sentence in output.sentences:
            sentence.knownType = "Not Periodic"
            allNewSentences.append(sentence)

        output.sentences = allNewSentences
    else:
        output = ProcessInput.process(text, textType)   
        output.sentences, score, numPeriodic = periodic.detectPeriodic(output.sentences, debug, argument, "Unknown") #We don't know the nature of the sentences
    
    if numPeriodic > 1:
        plural = "s"
    else:
        plural = ""

    output.summary += "\n" + str(numPeriodic) + " periodic sentence" + plural + " detected."
    end = time.time()
    print("Run time: " + str(end - start) + " seconds")
    if textType == "Test":
        return render_template('test.html', output=output, periodicScore=periodicScore, notPeriodicScore=notPeriodicScore, debug=debug, runtime=str(round(end - start)))
    elif outputFormat == 'html':
        return render_template('render.html', output=output, debug=debug, runtime=str(round(end - start)))
    elif outputFormat == 'sadface':
        return ProcessOutput.renderSADFace(output.sentences)
    else:
        return '<h2>Sorry, "' + outputFormat + '" is not a supported output format. Please specify "html" or "sadface" as the output format instead.<h2>'
    return flask.jsonify(sentences)

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
        return render_template('home.html')

@app.route('/render', methods=['GET'])
def Render():
    output = request.form['output']
    debug = request.form['debug']
    runtime = request.form['runtime']
    return render_template('render.html', output=output, debug=debug, runtime=runtime)

@app.route('/test', methods=['GET'])
def Test():
    output = request.form['output']
    debug = request.form['debug']
    runtime = request.form['runtime']
    return render_template('test.html', output=output, debug=debug, runtime=runtime)
app.run()
