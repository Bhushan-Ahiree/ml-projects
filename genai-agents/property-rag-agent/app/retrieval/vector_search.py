import numpy as np

def cosine_similarity(query_embedding, property_embeddings):
    similarities = np.dot(property_embeddings, query_embedding) / (
        np.linalg.norm(property_embeddings, axis=1)
        * np.linalg.norm(query_embedding)
    )

    
    return similarities

def retrieve_top_k(query_embedding, property_embeddings, k=5):
    similarities = cosine_similarity(
        query_embedding, 
        property_embeddings
    )
    
    top_indices = np.argsort(similarities)[::-1][:k]
    
    return top_indices, similarities[top_indices]