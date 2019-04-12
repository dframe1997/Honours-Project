import nltk
import flask
from flask import render_template, url_for, request, redirect, abort, json, flash
from Canary import URLDownloader, OutputFormat, periodic

app = flask.Flask(__name__)
app.config["DEBUG"] = True

nltk.data.path.append(r"D:\Users\David\Documents\Work\University\Year 4\Honours\NLTK")

@app.route('/', methods=['GET'])
def API():
    url = request.args['url']
    outputFormat = request.args['outputFormat']
    output = URLDownloader.processURL(url)   
    output.sentences = periodic.process(output.sentences); 
    if outputFormat == 'html':
        return render_template('render.html', output=output)
    elif outputFormat == 'json':
        return 'JSON OUTPUT';
    else:
        return '<h2>Sorry, "' + outputFormat + '" is not a supported type. Please include "html" or "json" as the output type.<h2>'
    return flask.jsonify(output)

@app.route('/home', methods=['POST','GET'])
def Home():
    if request.method == 'POST':
        print(request.form)
        url = request.form['url']
        return redirect(url_for('.API', url=url, outputFormat='html'))
    else:
        return render_template('home.html')

@app.route('/render', methods=['GET'])
def Render():
    output = request.form['output']
    return render_template('render.html', output=output)
app.run()
