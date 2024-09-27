# import docker

# client = docker.Client(base_url='unix://var/run/docker.sock')

# containers = client.containers()

# for container in containers:
#     print(container)

# # Try to access some other attributes/methods of the client
# # print(client.version())
# # print(client.info())

# import docker

# print(docker.__version__)

# client = docker.from_env()
# print(type(client))
# print(dir(client.images))


# import docker

# client = docker.from_env()

# # Run a container based on the 'python:3.9' image
# container = client.containers.run("python:3.9", "python -c 'print(\"Hello from Docker!\")'", detach=True)

# # Get the container logs
# logs = container.logs()
# print(logs.decode('utf-8'))



# from python_on_whales import docker
# import time

# output = docker.run("hello-world")


# time.sleep(1000)
# print(output)



print("hey it is working")