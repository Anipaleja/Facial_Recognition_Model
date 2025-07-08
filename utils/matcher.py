import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def match_face(embedding, database, threshold=0.5):
    best_match = ("Unknown", 0)
    for name, db_embedding in database.items():
        sim = cosine_similarity([embedding], [db_embedding])[0][0]
        if sim > best_match[1] and sim >= threshold:
            best_match = (name, sim * 100)
    return best_match
