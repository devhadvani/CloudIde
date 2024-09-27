# tasks.py in your app

from celery import shared_task
import time
from .models import Blog

@shared_task
def create_blog_post(blog_id, title, description, img_path):
    time.sleep(10)
    print("i am comming here")
    blog = Blog.objects.get(id=blog_id)
    blog.title = title
    blog.description = description
    blog.img = img_path
    blog.status = 'Completed'
    blog.save()
    return "Blog created successfully"
@shared_task
def add(x, y):
    print(f"x = {x} and y = {y} ")
    time.sleep(10)
    return x + y

