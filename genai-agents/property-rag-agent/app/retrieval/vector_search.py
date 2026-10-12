import numpy as np

def cosine_similarity(query_embedding, property_embeddings):
    # Added a small epsilon to prevent division by zero if an embedding is all zeros
    norm_props = np.linalg.norm(property_embeddings, axis=1)
    norm_query = np.linalg.norm(query_embedding)
    
    return np.dot(property_embeddings, query_embedding) / (norm_props * norm_query + 1e-9)

def retrieve_top_k(query_embedding, property_embeddings, k=5, properties=None, city=None, max_price=None, bhk=None):
    mask = np.ones(len(property_embeddings), dtype=bool)

    # Apply city filter if provided
    if city is not None and properties is not None:
        mask &= (properties["city"].str.lower() == city.lower()).to_numpy()
        
    # Apply price filter if provided
    if max_price is not None and properties is not None:
        mask &= (properties["price"].to_numpy() <= max_price)
    
    if bhk is not None:
        mask &= (
            properties["house_type"]
            .str.extract(r"(\d+)\s*BHK", expand=False)
            .fillna("-1")
            .astype(int)
            .to_numpy() == bhk
        )

    # Filter the embeddings and keep track of original indices
    candidate_embeddings = property_embeddings[mask]
    candidate_indices = np.where(mask)[0]

    # Handle case where no properties match the criteria
    if len(candidate_embeddings) == 0:
        return np.array([]), np.array([])

    # Calculate similarities only for filtered candidates
    similarities = cosine_similarity(query_embedding, candidate_embeddings)

    # Sort and get top K
    actual_k = min(k, len(similarities))
    top_positions = np.argsort(similarities)[::-1][:actual_k]

    return (
        candidate_indices[top_positions],
        similarities[top_positions]
    )
