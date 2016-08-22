#My project will use the NY Times Most Popular API in order to find the most viewed article, most shared article,
#and most emailed article. The user will have the option to pick their range of time for the articles and then the 
#terminal window will display a list of articles, authors, publishing dates and tags in descending order.
#I will then use the keywords or tags of these articles and search for tweets with these keywords. 
#I will then analyze the tweets and give each keyword a positive or negative score based on the contents
#of the tweets.


import test
import sys
import urllib
import urllib2
import json
import oauth2

#Get all words from positive word list
pos_ws = []
f = open('positive-words.txt', 'r')

for l in f.readlines()[35:]:
    pos_ws.append(unicode(l.strip()))
f.close()

#Get all words from negative word list

neg_ws = []
f = open('negative-words.txt', 'r')
for l in f.readlines()[35:]:
    neg_ws.append(unicode(l.strip()))


#Create a class called Keyword. 
#Each instance of the keyword class is a tag from the list of top 20 most viewed NY Times articles.
#The keyword_twittersearch will call the function get_tweets which returns a list of tweets with the keyword.
#The calculateEmoScore will iterate through the tweets and the pos/neg words list in order to see if any positive words or negative words are in that tweet.
#It will then calculate a score for that keyword.
class Keyword:
 	keyword = ""
 	pos_ws = 0
 	neg_ws = 0
 	
 	def __init__(self, keyword_in):
 		self.keyword = keyword_in
 		self.keyword_twittersearch()
 		
 	def calculateEmoScore(self, tweet):
 		for word in tweet.split():
 			if word in pos_ws:
 				self.pos_ws = self.pos_ws +1
 			elif word in neg_ws:
 				self.neg_ws = self.neg_ws +1
 	
 	def keyword_twittersearch(self):
 		tempList = get_tweets(self.keyword)['statuses']
		for status in tempList:
			self.calculateEmoScore(status['text'])
	def __str__(self):
		return self.keyword

 
#Get article data in JSON dictionary for one 30 days
def get_article(x): 
	baseurl = 'http://api.nytimes.com/svc/mostpopular/'
	version = 'v2/'
	resource_type = x
	section = 'all-sections/'
	time_period = '30'	
	api_key = '245c8cfa5c6c35c05c4d473e257e013c:12:70288144'
	article_request = baseurl + version + resource_type + section + time_period + '.json?api-key=' + api_key 
	result = urllib2.urlopen(article_request).read()
	article_data = json.loads(result)
	return article_data
	
#Get article data in JSON dictionary for 7 days
def get_article_week(x): 
	baseurl = 'http://api.nytimes.com/svc/mostpopular/'
	version = 'v2/'
	resource_type = x
	section = 'all-sections/'
	time_period = '7'
	api_key = '245c8cfa5c6c35c05c4d473e257e013c:12:70288144'
	article_request = baseurl + version + resource_type + section + time_period + '.json?api-key=' + api_key 
	result = urllib2.urlopen(article_request).read()
	article_data = json.loads(result)
	return article_data

#Get article data in JSON dictionary for one day
def get_article_day(x): 
	baseurl = 'http://api.nytimes.com/svc/mostpopular/'
	version = 'v2/'
	resource_type = x
	section = 'all-sections/'
	time_period = '1'
	api_key = '245c8cfa5c6c35c05c4d473e257e013c:12:70288144'
	article_request = baseurl + version + resource_type + section + time_period + '.json?api-key=' + api_key 
	result = urllib2.urlopen(article_request).read()
	article_data = json.loads(result)
	return article_data

#Get tweets that have the keyword in them.
def get_tweets(input):
	CONSUMER_KEY = "jz2rnCUkEoxMwOdSotlVvkdPC"
	CONSUMER_SECRET = "60Uwmgm6OAXgeryyNFbnBy815CRun3iatJtvy2JWDUcYj4R5h0"
	TOKEN = "1363213442-AfhSEqOMy6L6F8qJwuS9sdejqrTaCCL1KOzUpYS"
	TOKEN_SECRET = "8mXke5lhyUrFyRvBm9ZHVhhELQN6Ru345da8MnUnhv0E2"
	consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
	token = oauth2.Token(TOKEN, TOKEN_SECRET)
	url = "https://api.twitter.com/1.1/search/tweets.json?"
	search_keys = {
    	'q': input,
	    'count': 10
	}
	oauth_request = oauth2.Request(method="GET", url=url, parameters=search_keys)
	oauth_request.update(
    	{
        	'oauth_consumer_key': CONSUMER_KEY,
        	'oauth_token': TOKEN,
	        'oauth_timestamp': oauth2.generate_timestamp(),
    	    'oauth_nonce': oauth2.generate_nonce()
    	}
	)
	oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)

	signed_url = oauth_request.to_url()     
	connection = urllib2.urlopen(signed_url)
	try:
		d = json.loads(connection.read())
		return d
	finally:
		connection.close()

#function to make JSON dictionary easier on the eyes
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

#Get all titles from Json dictionary
def get_titles(article):
	titles = []

	for x in range(0,20):
		titles.append(article['results'][x]['title'])
	return titles

#Get all authors from JSON dictionary
def get_authors(article):
	authors = []

	for x in range(0,20):
		authors.append(article['results'][x]['byline'])
	return authors

#Get all tags from JSON dictionary	
def get_tags(article):
	tags = []
	
	for x in range(0,20):
		tags.append(article['results'][x]['des_facet'])
	return tags

#Get all publishing dates from JSON dictionary
def get_publish_dates(article):
	publish_dates = []

	for x in range(0,20):
		publish_dates.append(article['results'][x]['published_date'])
	return publish_dates

#get all keyword tags from article
def get_keywords(article):
	keyword = {}
	for x in range(0,20):
		for word in article['results'][x]['des_facet']:
			if word in keyword:
				keyword[word] = keyword[word] + 1
			else:
				keyword[word] = 1
	return keyword

option = 0

#Simple interface menu
while option != 5:
	option = int(raw_input("Main Menu : \n 1 - Show Most Shared Article from the New York Times \n 2 - Show Most Viewed Article from the New York Times \n 3 - Show Most Emailed Article from The New York Times\n 4 - Show Emo Scores for NY Times Key Words on Twitter \n 5 - Quit \n Enter: "))

	#article = get_article('mostshared/')

	# 1) View Most Shared Article
	# 		Display title name, author, publish date, 
	if option == 1:
		option_2=0
		while option_2 != 4:
			option_2 = int(raw_input("Choose a time period: \n 1 - One Day \n 2 - One Week \n 3 - One Month \n 4 - Go back \n Enter: "))		
			if option_2 == 1:
					print 'Top 20 Most Shared Articles from The New York Times (in the last day): \n' + '----------------------------------------- \n'
					article = get_article_day('mostshared/')
					titles = get_titles(article)
					authors = get_authors(article)
					publish_dates = get_publish_dates(article)
					tag = get_tags(article)
		
					for x in range(0,20):
						print str(x+1) + ') ' + titles[x] + '\n' 
						print '   ' + authors[x] + '\n'
						print '   ' + publish_dates[x] + '\n'
						print 'The tags of this article are: ' + str(tag[x]) + '\n'
						print '___________________________________'
			if option_2 == 2:
					print 'Top 20 Most Shared Articles from The New York Times (in the last week): \n' + '----------------------------------------- \n'
					article = get_article_week('mostshared/')
					titles = get_titles(article)
					authors = get_authors(article)
					publish_dates = get_publish_dates(article)
					tag = get_tags(article)
		
					for x in range(0,20):
						print str(x+1) + ') ' + titles[x] + '\n' 
						print '   ' + authors[x] + '\n'
						print '   ' + publish_dates[x] + '\n'
						print 'The tags of this article are: ' + str(tag[x]) + '\n'
						print '___________________________________'
			if option_2 == 3:
					print 'Top 20 Most Shared Articles from The New York Times (in the last month): \n' + '----------------------------------------- \n'
					article = get_article('mostshared/')
					titles = get_titles(article)
					authors = get_authors(article)
					publish_dates = get_publish_dates(article)
					tag = get_tags(article)
		
					for x in range(0,20):
						print str(x+1) + ') ' + titles[x] + '\n' 
						print '   ' + authors[x] + '\n'
						print '   ' + publish_dates[x] + '\n'
						print 'The tags of this article are: ' + str(tag[x]) + '\n'
						print '___________________________________'
	

	# 2) Show Most Viewed Article
	#		Display title name, author, publish date, abstract
	elif option == 2:
		option_3=0
		while option_3 != 4:
			option_3 = int(raw_input("Choose a time period: \n 1 - One Day \n 2 - One Week \n 3 - One Month \n 4 - Go back \n Enter: "))		
			if option_3 == 1:
					print 'Top 20 Most Viewed Articles from The New York Times (in the last day): \n' + '----------------------------------------- \n'
					article = get_article_day('mostviewed/')
					titles = get_titles(article)
					authors = get_authors(article)
					publish_dates = get_publish_dates(article)
					tag = get_tags(article)
		
					for x in range(0,20):
						print str(x+1) + ') ' + titles[x] + '\n' 
						print '   ' + authors[x] + '\n'
						print '   ' + publish_dates[x] + '\n'
						print 'The tags of this article are: ' + str(tag[x]) + '\n'
						print '___________________________________'
			if option_3 == 2:
					print 'Top 20 Most Viewed Articles from The New York Times (in the last week): \n' + '----------------------------------------- \n'
					article = get_article_week('mostviewed/')
					titles = get_titles(article)
					authors = get_authors(article)
					publish_dates = get_publish_dates(article)
					tag = get_tags(article)
		
					for x in range(0,20):
						print str(x+1) + ') ' + titles[x] + '\n' 
						print '   ' + authors[x] + '\n'
						print '   ' + publish_dates[x] + '\n'
						print 'The tags of this article are: ' + str(tag[x]) + '\n'
						print '___________________________________'
			if option_3 == 3:
					print 'Top 20 Most Viewed Articles from The New York Times (in the last month): \n' + '----------------------------------------- \n'
					article = get_article('mostviewed/')
					titles = get_titles(article)
					authors = get_authors(article)
					publish_dates = get_publish_dates(article)
					tag = get_tags(article)
		
					for x in range(0,20):
						print str(x+1) + ') ' + titles[x] + '\n' 
						print '   ' + authors[x] + '\n'
						print '   ' + publish_dates[x] + '\n'
						print 'The tags of this article are: ' + str(tag[x]) + '\n'
						print '___________________________________'
	
	# 3) Show Most Emailed Article
	#		Display title name, author, publish date, abstract 
	elif option == 3:
		option_4=0
		while option_4 != 4:
			option_4 = int(raw_input("Choose a time period: \n 1 - One Day \n 2 - One Week \n 3 - One Month \n 4 - Go back \n Enter: "))		
			if option_4 == 1:
					print 'Top 20 Most Emailed Articles from The New York Times (in the last day): \n' + '----------------------------------------- \n'
					article = get_article_day('mostemailed/')
					titles = get_titles(article)
					authors = get_authors(article)
					publish_dates = get_publish_dates(article)
					tag = get_tags(article)
		
					for x in range(0,20):
						print str(x+1) + ') ' + titles[x] + '\n' 
						print '   ' + authors[x] + '\n'
						print '   ' + publish_dates[x] + '\n'
						print 'The tags of this article are: ' + str(tag[x]) + '\n'
						print '___________________________________'
			if option_4 == 2:
					print 'Top 20 Most Emailed Articles from The New York Times (in the last week): \n' + '----------------------------------------- \n'
					article = get_article_week('mostemailed/')
					titles = get_titles(article)
					authors = get_authors(article)
					publish_dates = get_publish_dates(article)
					tag = get_tags(article)
		
					for x in range(0,20):
						print str(x+1) + ') ' + titles[x] + '\n' 
						print '   ' + authors[x] + '\n'
						print '   ' + publish_dates[x] + '\n'
						print 'The tags of this article are: ' + str(tag[x]) + '\n'
						print '___________________________________'
			if option_4 == 3:
					print 'Top 20 Most Emailed Articles from The New York Times (in the last month): \n' + '----------------------------------------- \n'
					article = get_article('mostemailed/')
					titles = get_titles(article)
					authors = get_authors(article)
					publish_dates = get_publish_dates(article)
					tag = get_tags(article)
		
					for x in range(0,20):
						print str(x+1) + ') ' + titles[x] + '\n' 
						print '   ' + authors[x] + '\n'
						print '   ' + publish_dates[x] + '\n'
						print 'The tags of this article are:  qq' + str(tag[x]) + '\n'
						print '___________________________________'
	


	# 4) #Shows keyword search and Emo score
	
	elif option == 4:
		header = 'NY Times keywords and their respective twitter emotional score (in the last month): '
		print header
		print len(header) * '-'
		article = get_article('mostviewed/')
		keyword_dict = get_keywords(article)
		keyword_list = [Keyword(tweet) for tweet in keyword_dict]
		sorted_list = sorted(keyword_list, key = lambda x: x.pos_ws- x.neg_ws, reverse = True)
		
		for item in sorted_list:
			print  item.keyword  ,  (item.pos_ws - item.neg_ws)
			
			
	#elif option == 6:
	
		print 'Goodbye'

	#print pretty(article)

	#status = 0


# ac = Keyword("puppy")
# test.testEqual(ac.keyword, 'puppy')
# test.testEqual(type(ac.keyword), type('instance'))

# bc = get_tweets(1)
# test.testEqual(type(bc),type({}))