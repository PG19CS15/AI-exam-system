import gensim
import numpy as np

# Load the saved Doc2Vec model
model = gensim.models.Doc2Vec.load('E:/doc2vec_model')

# Define a function to infer vectors for new documents
def infer_vector(doc):
    return model.infer_vector(doc.split())

# Example usage
doc1 = "This is an example document."
doc2 = "the cat is walking."
vec1 = infer_vector(doc1)
vec2 = infer_vector(doc2)
similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
print("Similarity between the two documents:", similarity)
