from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),


    path('task1', views.Task1.as_view(), name='task1'),
    path('execute_task1', views.execute_task1, name='ExecuteTask1'),

    path('task2', views.Task2.as_view(), name='task2'),
    path('execute_task1', views.execute_task1, name='ExecuteTask2'),

    path('task3', views.Task3.as_view(), name='task3'),
    path('execute_task3', views.execute_task3, name='ExecuteTask3'),

    path('task4', views.Task4.as_view(), name='task4'),
    path('execute_task4', views.execute_task4, name='ExecuteTask4'),

    path('task5', views.Task5.as_view(), name='task5'),
    path('execute_task5', views.execute_task5, name='ExecuteTask5'),

    path('task6', views.Task6.as_view(), name='task6'),
    path('execute_task6', views.execute_task6, name='ExecuteTask6'),

]
