import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
# Load training data
train_data = pd.read_csv("student_answers_train.csv")
X_train = train_data['student_answer']
y_train = train_data['score']

# Load testing data
test_data = pd.read_csv("student_answers_test.csv")
X_test = test_data['student_answer']

# Define text preprocessing function
def preprocess_text(text):
    # Tokenize text
    tokens =nltk.wordpunct_tokenize(text)
    
    # Remove stop words and lemmatize tokens
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    
    # Return preprocessed text
    return ' '.join(tokens)

# Preprocess text data
X_train = [preprocess_text(text) for text in X_train]
X_test = [preprocess_text(text) for text in X_test]

# Create pipeline with feature selection (removing low-frequency words)
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(min_df=2)),
    ('reg', LinearRegression())
])

# Train model on training data
pipeline.fit(X_train, y_train)

# Evaluate model on testing data
y_pred = pipeline.predict(X_test)

print(y_pred)