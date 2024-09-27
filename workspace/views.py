from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt
import subprocess
from .tasks import add,create_blog_post
from .forms import BlogForm
from .models import Blog
import time
def home(request):
    print("beofre taks")
    task = add.delay(5,10)
    print("task",task)
    return render(request,'index.html')


def create_blog_view(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            # time.sleep(5)
            # blog = form.save()
            blog = form.save(commit = False)  
            blog.status = 'Pending'
            blog.save()
 
            create_blog_post.delay(blog.id, blog.title, blog.description, blog.img.name)
            return HttpResponse('blog created')
    else:
        form = BlogForm()

    return render(request, 'create_blog.html', {'form': form})

def template_editor(request):
    return render(request, 'editor.html')

def save_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        filename = 'template.html'
        print(code)
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        response.write(code)
        return response

    return HttpResponse("Only POST requests are allowed", status=405)
    

def run_code(request):
    if request.method == "POST":
        code = request.POST.get('code', '')
        try:
            print(code)
            output = subprocess.run(['python3','-c',code], text=True, capture_output=True, check=True)
            print(output)
            output = output.stdout

        except subprocess.CalledProcessError as e:
            output = e.stderr or 'An error occurred while executing the code.'
            
        return JsonResponse({'output':output})



@csrf_exempt
def execute_command(request):
    if request.method == 'POST':
        command = request.POST.get('command', '').strip()
        current_directory = request.POST.get('current_directory', '/')

        if command.startswith('cd '):
            # Handle directory change
            new_dir = command[3:].strip()
            if new_dir.startswith('/'):
                full_path = new_dir
            else:
                full_path = os.path.join(current_directory, new_dir)
            
            if os.path.isdir(full_path):
                return JsonResponse({
                    'output': f'Changed directory to {full_path}',
                    'new_directory': full_path
                })
            else:
                return JsonResponse({
                    'output': f'Directory not found: {full_path}',
                    'new_directory': current_directory
                })
        
        try:

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=current_directory
            )
            stdout, stderr = process.communicate(timeout=1000)
            
            if process.returncode == 0:
                output = stdout
            else:
                output = f"Error: {stderr}"
            
            return JsonResponse({
                'output': output,
                'new_directory': current_directory
            })
        
        except subprocess.TimeoutExpired:
            return JsonResponse({
                'output': 'Command execution timed out',
                'new_directory': current_directory
            })
        except Exception as e:
            return JsonResponse({
                'output': f'Error: {str(e)}',
                'new_directory': current_directory
            })

    return JsonResponse({'error': 'Invalid request method'})
import docker
from django.http import JsonResponse

# def start_container(request):
#     client = docker.from_env()
#     print("client:", client)
    
#     environment = "djangmo"
    
#     try:
#         if environment == 'django':

#             print("in the djanfgo")
#             container = client.create_container(
#                 image='python:3.9',
#                 command='django-admin startproject myproject',
#                 volumes=['/path/to/local/folder:/usr/src/app'],
#                 host_config=client.create_host_config(
#                     binds={'/path/to/local/folder': {'bind': '/usr/src/app', 'mode': 'rw'}}
#                 )
#             )
#             print("it wos")
#         else:  # Assuming 'react' is the alternative
#             container = client.create_container(
#                 image='node:14',
#                 command='npx create-react-app myapp',
#                 volumes=['/path/to/local/folder:/usr/src/app'],
#                 host_config=client.create_host_config(
#                     binds={'/path/to/local/folder': {'bind': '/usr/src/app', 'mode': 'rw'}}
#                 )
#             )
        
#         client.start(container=container.get('Id'))
        
#         print("Container:", container)
#         return JsonResponse({'container_id': container.get('Id')})
    
#     except docker.errors.APIError as e:
#         return JsonResponse({'error': str(e)}, status=500)
#     except Exception as e:
#         return JsonResponse({'error': f"An unexpected error occurred: {str(e)}"}, status=500)



# def start_container(request):
#     try:
#         # Connect to Docker using the Docker client
#         client = docker.from_env()
        
#         # Specify the container name or ID you want to start
#         container_name = "flask-docker-web"  # Replace with the desired container name or ID
#         print(client)
#         # Get the container object by name or ID
#         print(client.containers)
#         container = client.containers.get(container_name)
        
#         # Start the container
#         container.start()
        
#         # Optionally, you can also attach to the container to get the logs or other information
#         logs = container.logs().decode('utf-8')
        
#         return JsonResponse({'status': 'Container started', 'logs': logs})
    
#     except docker.errors.NotFound:
#         return JsonResponse({'error': f"Container '{container_name}' not found"}, status=404)
#     except docker.errors.APIError as e:
#         return JsonResponse({'error': str(e)}, status=500)
#     except Exception as e:
#         return JsonResponse({'error': f"An unexpected error occurred: {str(e)}"}, status=500)


from python_on_whales import docker
from django.http import JsonResponse

def start_container(request):
    try:
        # Replace with the actual container ID
        container_id = "497f191626ce"

        # Start the container
        result_string = docker.run("django", ["python3","app/manage.py","runserver"], volumes=[("/home/bacancy/Desktop/ide/CloudIde", "/app", "rw")])
        # container = docker.run("django",[["django-admin", "startproject", "test", "."],["python3","manage.py","runserver"]])

        print(result_string)

        # List the files within the container

        # files = docker.execute(container_id, ["django-admin", "startproject", "test"])

        # filenames = [line.split()[-1] for line in files.splitlines()]

        # print(filenames)

        # Return a JsonResponse with the file listing
        return JsonResponse({'container_id': container_id, 'files': filenames})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)