# -*- coding: utf-8 -*
import nltk
from datetime import datetime, timedelta
import PhraseGenerator as pg
import summarizer as sm
from textblob import TextBlob


period = datetime.now() - timedelta(hours=6)


def get_db(db_name):
    from pymongo import MongoClient
    uri = 'mongodb://user:passw0rd@kahana.mongohq.com:10026/dev-ethinker'
    client = MongoClient(uri)
    db = client[db_name]
    return db  


def headlineGenerator(corpus, entity):
	gen = pg.PhraseGenerator(corpus, categories='news')
	return gen(entity)
		
		

def sentiment(content):
	text=TextBlob(content.decode("utf8"))
	text_en=text.translate(from_lang="es", to='en')
	return [text_en.sentiment.polarity,text_en.sentiment.subjectivity]


def contentGenerator(corpus):
		
	tokenized_content =corpus.split()
	content_model = nltk.NgramModel(3, tokenized_content)
	words_to_generate = 13 #int(len(tokenized_content)/9)

	starting_words = content_model.generate(200)[-2:]
	content = content_model.generate(words_to_generate, starting_words)
	return' '.join(content)


def newsGenerator():
	db = get_db('dev-ethinker')

	trends = db.trends.find().sort('date',-1).limit(1)
	output=[]
	for item in trends[0]['entities']:
		
		data = db.articles.find({"date":{"$gt": period},"entities" : item['entity']})
		articles=[]
		for content in data:
			dic={"content":""}
			dic['content']=content['content'].encode('utf8')
			articles.append(dic)


		corpus = ' '.join(article['content'] for article in articles)

		ss = sm.SimpleSummarizer()
		content=ss.summarize(corpus, 4)

		title=contentGenerator(corpus)

		sent=sentiment(content)
		#title=headlineGenerator(corpus,item['entity'])

		output = {'title':title,
			      'summary':content,
				  'sentiment':{'polarity':sent[0],'subjectivity':sent[1]},
				  'time':int(60*float(len(content.split()))/250),
				  'class':""}

		db.newarticles.insert(output)

		#print output

	



def main():
	newsGenerator()
	



if __name__ == '__main__':
	main()