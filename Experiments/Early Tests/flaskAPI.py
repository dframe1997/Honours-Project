from newspaper import Article
import nltk
import flask
from flask import render_template, url_for, request, redirect, abort, json, flash

app = flask.Flask(__name__)
app.config["DEBUG"] = True

nltk.data.path.append(r"D:\Users\David\Documents\Work\University\Year 4\Honours\NLTK")

def processURL(url):
    output = ""
    article = Article(url)
    article.download()

    #Printing article details
    #output += "----- Article HTML -----"
    #output += article.html + "<br />"
    output += "----- Parsed Details -----<br />"
    article.parse()
    output += "Author(s): " + str(article.authors) + "<br />"
    output += "Publish Date: " + str(article.publish_date) + "<br />"
    output += "Top image: " + article.top_image + "<br />"
    output += "Videos: " + str(article.movies) + "<br />"
    output += "----- Article Text -----<br />"
    output += article.text + "<br />"
    output += "----- Processed Information -----<br />"
    article.nlp()
    output += "Keywords: " + str(article.keywords) + "<br />"
    output += "Summary: " + article.summary + "<br />"
    output += "----- Sentence Split -----<br />"
    output = splitSentences(article.text, output)
    return output

def splitSentences(articleText, output):
    #Splitting the article into sentences
    sentences = articleText.split('.')
    for sentence in sentences:
        output += sentence + "<br />"

        tokens = nltk.word_tokenize(sentence)
        #output += tokens + """
#"""

        tagged = nltk.pos_tag(tokens)
        #output += tagged[0:6] + """
#"""

        entities = nltk.chunk.ne_chunk(tagged)
        #output += entities + """
#"""

        output += "---<br />"

        #from nltk.corpus import treebank
        #t = treebank.parsed_sents('wsj_0001.mrg')[0]
        #entities.draw()
    return output

@app.route('/', methods=['POST','GET'])
def entryPoint():
    url = request.args['url']
    output = processURL(url)
    return "<p>" + output + "</p>"
app.run()
