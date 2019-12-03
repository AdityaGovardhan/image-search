from database_connection import DatabaseConnection
import os
from histogram_of_gradients import HistogramOfGradients
from local_binary_pattern import LocalBinaryPattern
from multiprocessing import Process
import os
from pathlib import Path
import glob


class DataPreProcessor:
    def __init__(self):
        '''
        1) Read each image from data dir and put metadata in database table.
        2) Pass that image to each feature model to get a vector of dimension (1 * m)
        3) Pass this vector to all the dimension reduction technique to get latent semantics.
        4) Put this latent semantic of each image from each model and technique with its metadata inside database
        '''

        self.database_connection = DatabaseConnection()

        self.process_metadata()
        self.process_classification_metadata()

        self.DATABASE_IMAGES_PATH = str(Path(str(Path(os.getcwd()).parent) + "/images"))
        self.CLASSIFICATION_IMAGES_PATH = str(Path(str(Path(os.getcwd()).parent) + "/phase3_sample_data"))

        feature_models = []

        feature_models.append("histogram_of_gradients")
        # feature_models.append("histogram_of_gradients_30")

        processes = []
        for i, feature in enumerate(feature_models):
            processes.append(Process(target=self.perform_feature_model(feature)))
            processes[i].start()

        for i in range(len(processes)):
            processes[i].join()

        # classification specific

        charas = ["Labelled", "Unlabelled"]
        sets = ["Set1", "Set2", "Set3", "Set4"]

        for chara_ in charas:
            for set_ in sets:
                path = self.CLASSIFICATION_IMAGES_PATH + "/" + chara_ + "/" + set_

                feature_models = []

                feature_models.append("histogram_of_gradients" + "_" + chara_ + "_" + set_)
                feature_models.append("local_binary_pattern" + "_" + chara_ + "_" + set_)

                processes = []
                for i, feature in enumerate(feature_models):
                    processes.append(Process(target=self.perform_classification_feature_model(feature, path)))
                    processes[i].start()

                for i in range(len(processes)):
                    processes[i].join()


    # This function will read all the metadata of input images and put those metadata details in database.
    def process_metadata(self):
        csv_file_path = str(Path(str(Path(os.getcwd()).parent) + "/Data/HandInfo.csv"))
        connection = self.database_connection.get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""DROP Table IF EXISTS metadata;""")
        # Create metadata table
        cursor.execute("""CREATE TABLE IF NOT EXISTS metadata( 
                        id INT NOT NULL, 
                        age INT NOT NULL, 
                        gender TEXT NOT NULL, 
                        skinColor TEXT NOT NULL, accessories INT NOT NULL,
                        nailPolish INT NOT NULL,
                        aspectOfHand TEXT NOT NULL,
                        imageName TEXT NOT NULL,
                        irregularities INT NOT NULL,
                        PRIMARY KEY (imageName)
                        );
                        """)
        # file opened to avoid permission error in linux
        with open(csv_file_path, 'r') as f:
            next(f)
            cursor.copy_from(f, 'metadata', sep=',', null='')
        # cursor.execute("""copy metadata from '{}' csv header;""".format(csv_file_path))
        connection.commit()

    def process_classification_metadata(self):

        # metadata_files = ['labelled_set1.csv', 'labelled_set2.csv', 'unlabelled_set1.csv', 'unlabelled_set2.csv']
        data_folder = str(Path(str(Path(os.getcwd()).parent) + "/Data/phase3_sample_data"))
        extension = 'csv'
        os.chdir(data_folder)
        metadata_files = [os.path.basename(x) for x in glob.glob('*.{}'.format(extension))]

        connection = self.database_connection.get_db_connection()

        cursor = connection.cursor()

        for metadata_file in metadata_files:
            table_name = "metadata_" + metadata_file.split('.')[0]
            metadata_file_path = data_folder + "/" + metadata_file

            cursor.execute("DROP Table IF EXISTS " + table_name + ";")

            cursor.execute("""CREATE TABLE IF NOT EXISTS """ + table_name + """(
                            some_number INT,
                            id INT NOT NULL,
                            age INT NOT NULL,
                            gender TEXT NOT NULL,
                            skinColor TEXT NOT NULL,
                            accessories INT NOT NULL,
                            nailPolish INT NOT NULL,
                            aspectOfHand TEXT,
                            imageName TEXT NOT NULL,
                            irregularities INT NOT NULL,
                            PRIMARY KEY (imageName)
                            );
                            """)
            # file opened to avoid permission error in linux
            with open(metadata_file_path, 'r') as f:
                next(f)
                cursor.copy_from(f, table_name, sep=',', null='')
            # cursor.execute("""copy """ + table_name + """ from '{}' csv header;""".format(metadata_file_path))
            connection.commit()

    def perform_feature_model(self, feature):
        histogram_of_gradients = HistogramOfGradients(self.DATABASE_IMAGES_PATH)
        feature_vectors = histogram_of_gradients.get_image_vectors()

        self.database_connection.create_feature_model_table(feature)
        self.database_connection.insert_feature_data(feature, feature_vectors)

    def perform_classification_feature_model(self, feature, path):
        self.database_connection.create_feature_model_table(feature)
        if "histogram_of_gradients" in feature:
            histogram_of_gradients = HistogramOfGradients(path)
            feature_vectors = histogram_of_gradients.get_image_vectors()
        elif "local_binary_pattern" in feature:
            local_binary_pattern = LocalBinaryPattern(path)
            feature_vectors = local_binary_pattern.get_image_vectors()

        self.database_connection.insert_feature_data(feature, feature_vectors)


if __name__ == "__main__":
    print('Preprocessing....')
    data_preprocessor = DataPreProcessor()
    print('Preprocessed!')
