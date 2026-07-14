import numpy as np
import os
import config


def user_exists(username):
    file_path = os.path.join(config.EMBEDDING_FOLDER, f"{username}.npy")

    return os.path.exists(file_path)


def save_embeddings(username, embedding):
    file_path = os.path.join(config.EMBEDDING_FOLDER, f"{username}.npy")

    embedding = embedding.cpu().numpy()
    os.makedirs(config.EMBEDDING_FOLDER, exist_ok=True)
    np.save(file_path, embedding)

    print(f"Embedding save at : {file_path}")


def load_embedding(username):
    file_path = os.path.join(config.EMBEDDING_FOLDER, f"{username}.npy")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No embedding found for user {username}")

    embedding = np.load(file_path)

    return embedding
