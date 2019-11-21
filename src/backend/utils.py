import numpy as np
from scipy import spatial
import matplotlib.pyplot as plt
import matplotlib

from database_connection import DatabaseConnection
import os
from pathlib import Path
import pickle


ALPHA = 0.85
PICKLE_FILE_NAME = "page_rank_interim.pickle"

def get_image_directory():
    path = str(Path(str(Path(os.getcwd()).parent) + '/Data/images'))
    if (not os.path.exists(path)):
        os.mkdir(path)
    return path

def get_pickle_directory():
    path = str(Path(str(Path(os.getcwd()).parent) + '/Data/pickle'))
    if(not os.path.exists(path)):
        os.mkdir(path)
    return path

def get_euclidian_distance(vector1, vector2):
    return np.linalg.norm(vector1 - vector2)


def read_from_database(model,label=None):
    database_connection = DatabaseConnection()
   
    if label==None:
        img_data_matrix_dict=database_connection.get_object_feature_matrix_from_db(tablename=model)
        return img_data_matrix_dict

def get_dot_distance(vector1, vector2):
    return np.dot(vector1, vector2)


def get_cosine_similarity(vector1, vector2):
    return spatial.distance.cosine(vector1, vector2)



def plot_scree_test(eigen_values):
    num_vars = len(eigen_values)

    fig = plt.figure(figsize=(8, 5))
    sing_vals = np.arange(num_vars) + 1
    plt.plot(sing_vals, eigen_values, 'ro-', linewidth=2)
    plt.title('Scree Plot')
    plt.xlabel('K latent semantic')
    plt.ylabel('Eigenvalue')

    leg = plt.legend(['Eigenvalues from SVD'], loc='best', borderpad=0.3,
                     shadow=False, prop=matplotlib.font_manager.FontProperties(size='small'),
                     markerscale=0.4)
    leg.get_frame().set_alpha(0.4)
    plt.show()

def save_to_pickle(object_to_save, file_name):
    pickle_directory = get_pickle_directory()
    with open(os.path.join(pickle_directory,file_name), 'wb') as f:
        pickle.dump(object_to_save, f)
    f.close()

def read_from_pickle(file_name):
    pickle_directory = get_pickle_directory()
    with open(os.path.join(pickle_directory,file_name), 'rb') as f:
        data = pickle.load(f)
    f.close()
    return data
