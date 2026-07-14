from sklearn.metrics.pairwise import cosine_similarity
import config


def calculate_similarity(embedding1, embedding2):
    embedding1 = embedding1.reshape(1, -1)
    embedding2 = embedding2.reshape(1, -1)

    similarity = cosine_similarity(embedding1, embedding2)[0][0]

    return similarity


def is_authenticated(similarity_score):
    return similarity_score >= config.SIMILARITY_THRESHOLD
