import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
sent = "There once lived an old man and an old woman who were peasants and had to work hard to earn their daily bread. The old man used to go to fix fences and do other odd jobs for the farmers around, and while he was gone the old woman, his wife, did the work of the house and worked in their own little plot of land."
token=nltk.wordpunct_tokenize(sent)
print(token)
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
tokens = [lemmatizer.lemmatize(token) for token in token if token not in stop_words]
print(tokens)