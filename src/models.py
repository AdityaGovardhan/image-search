from django.db import models

# Create your models here.

classifiers = (
        ('Support Vector Machine', 'Support Vector Machine'),
        ('Decision Tree Classifier', 'Decision Tree Classifier'),
        ('Personalized Page Rank', 'Personalized Page Rank'),
    )

task_6_relevance_feedbacks = (
        ('Support Vector Machine', 'Support Vector Machine'),
        ('Decision Tree Classifier', 'Decision Tree Classifier'),
        ('Personalized Page Rank', 'Personalized Page Rank'),
        ('Probabilistic', 'Probabilistic'),
        ('None', 'None'),
    )

datasets = (
        ('set1', 'set1'),
        ('set2', 'set2'),
        ('set3', 'set3'),
        ('set4', 'set4'),
    )

kernels = (
    ('linear', 'linear'),
    ('poly', 'poly'),
    ('rbf', 'rbf'),
    ('gaussian', 'gaussian'),
    )

number_of_total_clusters = (
    ('200', '200'),
    ('250', '250'),
    ('300', '300'),
    )


class Task1Model(models.Model):
    number_of_latent_semantics = models.CharField(max_length=3, verbose_name="Number of Latent Semantics")
    labelled_dataset = models.CharField(max_length=6, choices=datasets, default='set1')
    Unlabelled_dataset = models.CharField(max_length=6, choices=datasets, default='set1')

class Task2Model(models.Model):
    number_of_clusters = models.CharField(max_length=2)
    labelled_dataset = models.CharField(max_length=6, choices=datasets, default='set1')
    Unlabelled_dataset = models.CharField(max_length=6, choices=datasets, default='set1')

class Task3Model(models.Model):
    most_similar_images = models.CharField(max_length=2, verbose_name = "Number of Most Similar Images")
    k = models.CharField(max_length=3, verbose_name="Number of outgoing Edges(k)")
    K = models.CharField(max_length=3, verbose_name="Number of most Dominant Images(K)")
    folder_name = models.CharField(max_length=100, verbose_name="Folder Path")
    user_images = models.CharField(max_length=200, verbose_name="User Preferred Images(Personalized)")


class Task4Model(models.Model):
    classifier = models.CharField(max_length=6, choices=classifiers, default='Support Vector Machine')
    dataset = models.CharField(max_length=6, choices=datasets, default='set1')
    number_of_clusters = models.CharField(max_length=6, choices=number_of_total_clusters, default='200')
    kernel = models.CharField(max_length=6, choices=kernels, default='linear')
    labelled_folder_name = models.CharField(max_length=100, verbose_name="Labelled Folder Path")
    unlabelled_folder_name = models.CharField(max_length=100, verbose_name="Unlabelled Folder Path")


class Task5Model(models.Model):
    number_of_layers = models.CharField(max_length=2)
    number_of_hashes_per_layer = models.CharField(max_length=2)
    query_image = models.CharField(max_length=100)
    most_similar_images = models.CharField(max_length=2, verbose_name = "Number of Most Similar Images")
    relevance_feedback = models.CharField(max_length=6, choices=task_6_relevance_feedbacks, default='None')


class Task6Model(models.Model):
    query_image = models.CharField(max_length=100)
    most_similar_images = models.CharField(max_length=2, verbose_name="Number of Most Similar Images")
    relevance_feedback = models.CharField(max_length=6, choices=task_6_relevance_feedbacks, default='Probabilistic')
    # pass


