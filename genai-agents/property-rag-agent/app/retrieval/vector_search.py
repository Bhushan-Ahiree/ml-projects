import numpy as np

def cosine_similarity(query_embedding, property_embeddings):
    similarity = np.dot(query_embedding, property_embeddings) / (
        np.linalg.norm(query_embedding) 
        * np.linalg.norm(property_embeddings, axis=1)
        )
    
    return similarity