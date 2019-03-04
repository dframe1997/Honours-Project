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
