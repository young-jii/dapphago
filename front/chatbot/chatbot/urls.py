
from django.contrib import admin
from django.urls import path, include
from board import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('board.urls')),
    path("get_botresponse", views.get_bot_response),
]
