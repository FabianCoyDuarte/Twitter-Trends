
import tweepy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
from collections import Counter

#Setting up the keys and tokens
c_k = "Consumer_Key"
c_s = "Consumer_Secret"

a_t = "Access_Token"
a_s = "Access_Token_Secret"
#Set Up Twitter API with keys and tokens
auth = tweepy.OAuthHandler(c_k, c_s)
auth.set_access_token(a_t, a_s)
api = tweepy.API(auth)


WORLD_WOE_ID = 1
US_WOE_ID = 23424977
MIAMI_WOE_ID = 2450022

# Using Tweepy api, It provites top 50 of trends in the Worlds, United States and Miami,
#  it is just to check tweet volumen and trends

# Funtions to extract features, data cleaning, and data sort. Next funtions were made 
# because the steps to analyse data will repeat more than twice.

# Funtion to extract information according to json file provided Tweepy API. it takes all information and creates a dataframe 
# just with Trends and Tweet volume. It is general information used to develop whole project.
def Extract_features(filter_json):
    trends = []
    TW_volume = []
    for names in filter_json:
        trends.append(names['name'])
        TW_volume.append(names['tweet_volume'])

    dic_list = {'Trends': trends, 'Tweet_volume': TW_volume}
    df = pd.DataFrame(dic_list)

    return df   

# Funtions to detect nulls and clean empty information
def detect_nulls(matx):
    return matx.isnull().any(axis=1).any()

def clean_data(matx):
    return matx.dropna()


# Funtion to sort data in ascending order, it is just to have a better view in chars
def sort_df(df):
    df = df.sort_values(by=['Tweet_volume'], ascending=False).reset_index(drop=True)
    return df

# World outcomes

#Extract specific features 
world_df = Extract_features(world_trends[0]['trends'])

#detect and delete nulls value in DataFrame
ans = True
try: 
    assert np.alltrue(detect_nulls(world_df) == ans)
except AssertionError as e: 
    print("Try again, your output did not match the expected answer above")

try: 
    world_df_cleaned=clean_data(world_df)
    assert np.alltrue(world_df_cleaned.shape[0] == 1064)
except AssertionError as e: 
    print("Try again")

#Sort values to have a good visualization in the char
world_df_cleaned = sort_df(world_df_cleaned)


#Plot DataFrame cleane and sort to identify behaviour of information 
plt.figure(figsize=[10,10])
plt.bar(world_df_cleaned['Trends'][:11],world_df_cleaned['Tweet_volume'][:11])

plt.xlabel('Trend',fontsize=20)
plt.xticks(rotation=90)
plt.ylabel('Tweet Volume',fontsize=20)
plt.title('Twitter Trends in the World',fontsize=30)
plt.grid(True)
plt.savefig('World_Tweets.png', dpi=1200 )
#plt.rcParams['font.sans-serif']=['SimHei']
plt.show()

# US Outcomes
#Extract specific features 
US_df = Extract_features(us_trends[0]['trends'])

#detect and delete nulls value in DataFrame
ans = True
try: 
    assert np.alltrue(detect_nulls(US_df) == ans)
except AssertionError as e: 
    print("Try again, your output did not match the expected answer above")

try: 
    US_df_cleaned=clean_data(US_df)
    assert np.alltrue(US_df_cleaned.shape[0] == 1064)
except AssertionError as e: 
    print("Try again")

#Sort values to have a good visualization in the char
US_df_cleaned = sort_df(US_df_cleaned)


#Plot DataFrame cleane and sort to identify behaviour of information 
plt.figure(figsize=[10,10])
plt.bar(US_df_cleaned['Trends'][:11],US_df_cleaned['Tweet_volume'][:11], color='r')
#barlist[0].set_color('r')
plt.xlabel('Trend',fontsize=20)
plt.xticks(rotation=90)
plt.ylabel('Tweet Volume',fontsize=20)
plt.title('Twitter Trends in United States',fontsize=30)
plt.grid(True)
plt.savefig('US_Tweets.png')
#plt.rcParams['font.sans-serif']=['SimHei']
plt.show()

# Miami outcomes
#Extract specific features 
MIAMI_df = Extract_features(miami_trends[0]['trends'])

#detect and delete nulls value in DataFrame
ans = True
try: 
    assert np.alltrue(detect_nulls(MIAMI_df) == ans)
except AssertionError as e: 
    print("Try again, your output did not match the expected answer above")

try: 
    MIAMI_df_cleaned=clean_data(MIAMI_df)
    assert np.alltrue(MIAMI_df_cleaned.shape[0] == 1064)
except AssertionError as e: 
    print("Try again")

#Sort values to have a good visualization in the char
MIAMI_df_cleaned = sort_df(MIAMI_df_cleaned)


#Plot DataFrame cleane and sort to identify behaviour of information 
plt.figure(figsize=[10,10])
plt.bar(MIAMI_df_cleaned['Trends'][:11],MIAMI_df_cleaned['Tweet_volume'][:11], color='g')
plt.xlabel('Trend',fontsize=20)
plt.xticks(rotation=90)
plt.ylabel('Tweet Volume',fontsize=20)
plt.title('Twitter Trends in Miami',fontsize=30)
plt.grid(True)
plt.savefig('Miami_Tweets.png')
#plt.rcParams['font.sans-serif']=['SimHei']
plt.show()

# Compare Trends between (World and Us) and (US and Miami)
#Connection between each place and How its influece affects global results

trends_set = {}
trends_set['world'] = set([trend['name'] for trend in world_trends[0]['trends']])

trends_set['us'] = set([trend['name'] for trend in us_trends[0]['trends']]) 

trends_set['miami'] = set([trend['name'] for trend in miami_trends[0]['trends']]) 

print(( '='*10,'intersection of world and us'))
print((trends_set['world'].intersection(trends_set['us'])))

print(('='*10,'intersection of us and miami'))
print((trends_set['miami'].intersection(trends_set['us'])))

inter_World_US= pd.merge(world_df_cleaned,US_df_cleaned,on=['Trends'])
inter_World_US.columns = ['Trends', 'World TW_volume','US TW_volume']
inter_World_US

#Outcome between global trends and american trends. It is just to check what porcentage is provided of US 
fig, ax = plt.subplots(figsize=(10,10))

x = np.arange(len(inter_World_US['Trends']))
width = 0.35
rects1 = ax.bar(x - width/2, inter_World_US['World TW_volume'], width, label='World Tweet Volume', color = 'green')
rects2 = ax.bar(x + width/2, inter_World_US['US TW_volume'], width, label='US Tweet Volume', color = 'gold')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Tweet Volume', fontsize = 25)
ax.set_xlabel('Trends', fontsize = 20)
ax.set_title('Diference between World and US Tweet volume',fontsize = 25)
ax.set_xticks(x)
ax.set_xticklabels(inter_World_US['Trends'], rotation = 90)
ax.grid(True)
ax.legend()

fig.savefig('Inter_World_US.png')

plt.show()

inter_US_Miami = pd.merge(US_df_cleaned, MIAMI_df_cleaned, on=['Trends'])
inter_US_Miami.columns = ['Trends', 'US TW_volume','Miami TW_volume']
print(inter_US_Miami.shape)
inter_US_Miami.head()

fig, ax = plt.subplots(figsize=(10,10))

x = np.arange(len(inter_US_Miami['Trends']))
width = 0.35
rects1 = ax.bar(x - width/2, inter_US_Miami['US TW_volume'], width, label='US Tweet Volume', color = 'navy')
rects2 = ax.bar(x + width/2, inter_US_Miami['Miami TW_volume'], width, label='Miami Tweet Volume', color = 'darkmagenta')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Tweet Volume', fontsize = 25)
ax.set_xlabel('Trends', fontsize = 20)
ax.set_title('Diference between US and Miami Tweet volume',fontsize = 30)
ax.set_xticks(x)
ax.set_xticklabels(inter_US_Miami['Trends'], rotation = 90)
ax.grid(True)
ax.legend()

fig.savefig('Inter_US_Miami.png')

plt.show()

# According to trending topic (Tropical Storm Elsa), analyse frecuency words and tweets results.

query = "ELSA"  # Hashtag of Tropial Storm Elsa

# Max number of tweets provide to Twitter, It will depend on you develop account
number = 900

search_results = tweepy.Cursor(api.search, q=query, lang="en").items(number)

#This will give us an Iterator
print(search_results)

# List of tweets, retweets and retweet counts that we will analyse 
tweets = []
retweeted = []
retweet_count = []

for tweet in search_results:
    tweets.append(tweet.text)
    retweet_count.append(tweet.retweet_count)
    # This if/else just checks the number of retweets and defines "rewteeted"
    # based on that value
    if tweet.retweet_count > 0:
        retweeted.append(True)
    else:
        retweeted.append(False)

ELSA_df_results = pd.DataFrame({'Tweet':tweets, 'Retweeted':retweeted, "Retweet Count":retweet_count})
ELSA_df_results.head()

True_Retweets = ELSA_df_results[ELSA_df_results['Retweeted'] == True].sort_values(by="Retweet Count", ascending=0).reset_index(drop=True)
True_Retweets[['Tweet','Retweet Count']]

False_Retweets = ELSA_df_results[ELSA_df_results['Retweeted'] == False].sort_values(by="Retweet Count", ascending=0).reset_index(drop=True)
False_Retweets[['Tweet','Retweet Count']]

# Look at most common complete Tweets and Retweets
def Print_Tweets_Counts(label, list_of_tuples):
    print("\n{:^50} | {:^10}".format(label, "Count"))
    print("*"*50)
    for k,v in list_of_tuples:
        print("{:10} | {:>6}".format(k,v))

for label, data in (('Tweet', True_Retweets['Tweet']), ('Retweet_count', True_Retweets['Retweet Count'])):
    c2 = Counter(data)
    Print_Tweets_Counts(label, c2.most_common()[:5])

for label, data in (('Tweet', False_Retweets['Tweet']), ('Retweet_count', False_Retweets['Retweet Count'])):
    c2 = Counter(data)
    Print_Tweets_Counts(label, c2.most_common()[:5])

# Loop to go across all tweets and check what unique post are according hashtag.
all_text = []
unique_tweets = []
for t in tweets:
    if not t in all_text:
        unique_tweets.append(t)
        all_text.append(t)
print(len(unique_tweets))

# Count the most common words in tweets according to Tropical Storm Elsa
#Split total words in a list
words = []
for t in tweets:
    for word in t.split():
        words.append(word)
        
c = Counter(words)
c.most_common(10)

def Print_Word_Count(label, list_of_tuples):
    print("\n{:^15} | {:^4}".format(label, "Count"))
    print("-"*25)
    for k,v in list_of_tuples:
        print("{:15} | {:>4}".format(k,v))


for label, data in (('Word', words), ('Retweet_count', retweet_count)):
    c = Counter(data)
    Print_Word_Count(label, c.most_common()[:10])