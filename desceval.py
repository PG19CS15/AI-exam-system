import pandas as pd
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error, r2_score
# Load training data
train_data = pd.read_csv("E:/student_answers_train.csv")
X_train = train_data[['student_answer', 'answer_key']]
y_train = train_data['score']

# Load testing data 
test_data = pd.read_csv("E:/student_answers_test.csv")
X_test = test_data['student_answer']
answer_key = test_data['answer_key']
# Define text preprocessing function
def preprocess_text(text):
    # Tokenize text
    tokens = nltk.wordpunct_tokenize(text)

    # Remove stop words and lemmatize tokens
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]

    # Return preprocessed text
    return ' '.join(tokens)

# Preprocess text data
X_train = [(preprocess_text(text[0]), preprocess_text(text[1])) for text in X_train.values]
X_test = [preprocess_text(text) for text in X_test]

# Define function to convert preprocessed text data to TaggedDocument format
def preprocess_for_doc2vec(texts):
    preprocessed_docs = []
    for i, text in enumerate(texts):
        preprocessed_docs.append(TaggedDocument(words=text.split(), tags=[i]))
    return preprocessed_docs

# Convert preprocessed text data to TaggedDocument format
train_docs = preprocess_for_doc2vec([text[0] for text in X_train] + [text[1] for text in X_train])
test_docs = preprocess_for_doc2vec(X_test)

# Train Doc2Vec model on training data
model = Doc2Vec(train_docs, vector_size=100, window=5, min_count=1, workers=4, epochs=20)

# Define function to calculate similarity score
def get_similarity_score(model, text1, text2):
    # Preprocess text data
    text1 = preprocess_text(text1)
    text2 = preprocess_text(text2)

    # Infer document vectors
    doc1_vector = model.infer_vector(text1.split())
    doc2_vector = model.infer_vector(text2.split())

    # Calculate cosine similarity score
    sim_score = cosine_similarity(doc1_vector.reshape(1, -1), doc2_vector.reshape(1, -1))[0][0]

    return sim_score

# Calculate similarity scores for student answers and answer key
# Calculate similarity scores for all student answers (including training data)
all_data = pd.concat([train_data, test_data], ignore_index=True)
all_X = all_data['student_answer']
all_answer_key = all_data['answer_key']

all_docs = preprocess_for_doc2vec(all_X)
model = Doc2Vec(all_docs, vector_size=100, window=5, min_count=1, workers=4, epochs=20)

all_sim_scores = []
for i, text in enumerate(all_X):
    sim_score = get_similarity_score(model, text, all_answer_key[i])
    all_sim_scores.append(sim_score)

# Normalize similarity scores to range [0, 1] and scale to match score range of 0-10
all_sim_scores = np.array(all_sim_scores)
all_sim_scores = (all_sim_scores - all_sim_scores.min()) / (all_sim_scores.max() - all_sim_scores.min())
all_y_pred = all_sim_scores

# Separate training and testing data in y_pred
train_y_pred = all_y_pred[:len(train_data)]
test_y_pred = all_y_pred[len(train_data):]

# Calculate mean squared error score for training data
mse = mean_squared_error(y_train, train_y_pred)

print("Mean squared error:", mse)

# Save the trained Doc2Vec model
model.save('E:/doc2vec_model')
# Save predictions for testing data to a CSV file
output_df = pd.DataFrame({'id': test_data['student_answer'], 'score': test_y_pred})
print(output_df.head())
