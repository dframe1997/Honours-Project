from newspaper import Article
import nltk

nltk.data.path.append(r"D:\Users\David\Documents\Work\University\Year 4\Honours\NLTK")

url = input("Input a URL: ")
article = Article(url)

article.download()
print("----- Article HTML -----")
print(article.html)
print("----- Parsed Details -----")
article.parse()
print("Author(s): " + str(article.authors))
print("Publish Date: " + str(article.publish_date))
print("Top image: " + article.top_image)
print("Videos: " + str(article.movies))
print("----- Article Text -----")
print(article.text)
print("----- Processed Information -----")
article.nlp()
print("Keywords: " + str(article.keywords))
print("Summary: " + article.summary)
print("----- Sentence Split -----")
#Splitting the article into sentences
sentences = article.text.split('.')
for sentence in sentences:
    print(sentence)

    tokens = nltk.word_tokenize(sentence)
    print (tokens)

    tagged = nltk.pos_tag(tokens)
    print (tagged[0:6])

    entities = nltk.chunk.ne_chunk(tagged)
    print(entities)

    print("---")

    #from nltk.corpus import treebank
    #t = treebank.parsed_sents('wsj_0001.mrg')[0]
    #entities.draw()
