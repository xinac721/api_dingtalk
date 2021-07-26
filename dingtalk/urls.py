from django.urls import path

import dingtalk.views

urlpatterns = [
    path('dingding', dingtalk.views.index),
    path('dingtalk', dingtalk.views.index),
]
