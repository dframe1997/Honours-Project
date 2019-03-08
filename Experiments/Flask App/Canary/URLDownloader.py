from newspaper import Article
from Canary import OutputFormat, SentenceFormat
import nltk

nltk.data.path.append(r"D:\Users\David\Documents\Work\University\Year 4\Honours\NLTK")

def processURL(url):
    article = Article(url)
    article.download()
    article.parse()   
    article.nlp()
    sentences = processSentences(article.text)

    output = OutputFormat.Output(url, article.title, article.authors, article.publish_date, article.top_image, article.movies, article.text, article.keywords, article.summary, sentences)
    return output

def processSentences(articleText):
    #Splitting the article into sentences
    sentencesText = articleText.split('.')
    sentences = []
    for sentence in sentencesText:      
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        entities = nltk.chunk.ne_chunk(tagged)

        newSentence = SentenceFormat.Sentence(sentence, tokens, tagged, entities)
        sentences.append(newSentence)
        #sentence.entities.draw()
    return sentences
