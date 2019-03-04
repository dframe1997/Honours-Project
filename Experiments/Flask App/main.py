from newspaper import Article
import nltk
import flask
from flask import render_template, url_for, request, redirect, abort, json, flash

app = flask.Flask(__name__)
app.config["DEBUG"] = True

nltk.data.path.append(r"D:\Users\David\Documents\Work\University\Year 4\Honours\NLTK")

class Output():  
    def __init__(self, url, author, publishDate, topImage, videos, text, keywords, summary, sentences):
        self.url = url
        self.author = author
        self.publishDate = publishDate
        self.topImage = topImage
        self.videos = videos
        self.text = text
        self.keywords = keywords
        self.summary = summary
        self.sentences = sentences
        
def processURL(url):
    article = Article(url)
    article.download()
    article.parse()   
    article.nlp()
    sentences = splitSentences(article.text)

    output = Output(url, article.authors, article.publish_date, article.top_image, article.movies, article.text, article.keywords, article.summary, sentences)
    return output

def splitSentences(articleText):
    #Splitting the article into sentences
    sentences = articleText.split('.')
    #for sentence in sentences:
        #output += sentence + "<br />"

        #tokens = nltk.word_tokenize(sentence)
        #output += tokens + """
#"""

        #tagged = nltk.pos_tag(tokens)
        #output += tagged[0:6] + """
#"""

        #entities = nltk.chunk.ne_chunk(tagged)
        #output += entities + """
#"""

        #output += "---<br />"

        #from nltk.corpus import treebank
        #t = treebank.parsed_sents('wsj_0001.mrg')[0]
        #entities.draw()
    return sentences

@app.route('/', methods=['POST','GET'])
def API():
    url = request.args['url']
    renderResponse = request.args['renderResponse']
    output = processURL(url)    
    if renderResponse == 'true':
        return render_template('render.html', output=output)
    return flask.jsonify(output)

@app.route('/home', methods=['POST','GET'])
def Home():
    if request.method == 'POST':
        print(request.form)
        url = request.form['url']
        algorithm = request.form['algorithm']
        return redirect(url_for('.API', url=url, algorithm=algorithm, renderResponse='true'))
    else:
        return render_template('home.html')

@app.route('/render', methods=['GET'])
def Render():
    output = request.form['output']
    return render_template('render.html', output=output)
app.run()
