import pickle
import os

def load_database(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    return {}

def save_database(db, path):
    with open(path, 'wb') as f:
        pickle.dump(db, f)