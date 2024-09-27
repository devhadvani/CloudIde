from .views import home,template_editor,save_code,run_code,start_container,execute_command, create_blog_view
from django.urls import path

urlpatterns = [
    path('',home),
    path('template_editor/',template_editor),
    path('save_code/',save_code,name="save_code"),
    path('run_code/',run_code,name="run_code"),
    path('start_container/',start_container),
    path('start_container/<str>:environment/',start_container),
    path('execute_command/', execute_command, name='execute_command'),
    path('create_blog/', create_blog_view, name='create_blog')
] 