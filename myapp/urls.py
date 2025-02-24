from django.urls import path
from .views import GeneralListCreateView,HomePageView, FirstFiveRecordsView,GetQueueNumberView,get_first_generic_list_item
from . import views
urlpatterns=[
    
    # path('', HomePageView.as_view(), name='home'),

    path('create/',GeneralListCreateView.as_view()),
    path('send_message/',FirstFiveRecordsView.as_view()),
    path('get_queue_number/', GetQueueNumberView.as_view(), name='get_queue_number'),
    path('get_first_item/', get_first_generic_list_item, name='get_first_item'),
    path('',views.home,name="home"),
    path('application',views.task_list,name="application"),
    path("login/", views.user_login, name="login"),
    path("complete_task/<int:task_id>/", views.complete_task, name="complete_task"),
    path("home_save/",views.HomeSave,name="home_save"),
    path("complete_work/<int:task_id>/",views.complete_work,name="complete_work"),
    path("cancelled_task/<int:task_id>/",views.cancelled_task,name="cancelled_task"),
    path("notcome_task/<int:task_id>/",views.notcome_task,name="notcome_task"),
    path("charts/",views.statistics_view,name="chart"),
    path("statistics/",views.get_statistics_data),
    
]