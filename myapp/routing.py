from django.urls import re_path
from .consumers import TaskConsumer  # Consumer faylingizni import qiling

ws_urlpatterns = [
    re_path(r"ws/task-updates/$", TaskConsumer.as_asgi()),  
]
