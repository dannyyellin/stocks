import datetime
import os
import shutil
from helpers import generate_requirements_file
import docker
import subprocess
import time


def remove_old_image(image_name):
    client = docker.from_env()
    try:
        img = client.images.get(image_name)
    except docker.errors.ImageNotFound:
        print(f"No image named {image_name} found")
        return
    try:
        client.images.remove(image_name, force = True)
        print(f"removed image {image_name}")
    except:
        print(f"Could not delete image named {image_name}")


def is_container_running(container_name):
    """
    Checks if a container is running.  Note we do not check the port it is listening at, although we could do that.
    Args:
        container_name: Name of the container.
    Returns:
        True if the container is running, False otherwise.
    """
    running = False
    # see https://docker-py.readthedocs.io/en/stable/containers.html for attributes available
    client = docker.from_env()
    if client.containers.list() == []:
        print("no containers in containers.list")
    for container in client.containers.list():
        # print(f"container attrs are {container.attrs}")
        Name = container.attrs.get('Name')
        Status = container.attrs.get('State')['Status']
        # Port = container.attrs.get('NetworkSettings')['Ports']
        print(f"Container {Name} has Status {Status}")
        # print("port = ", Port)
        if Name == container_name and Status == 'running':
            running = True
            # print(f"Container with name = {container_name} is running")
    # if not running:
    #     print(f"No container with name = {container_name} exists")
    return running


d = datetime.now()
curtime = d.strftime("%d-%m-%Y?-%M%S")
base_dir = "/Users/danielyellin/PycharmProjects/stocks/"
code_sub_dir = '13-11-2024?-4122-gpt4-temp0.5-1tok5000-2tok4000/'
service_name = 'stocks'
file_name_wo_ext = 'stocks-s1-v0'
code_pathnm = base_dir + sub_dir + file_name_wo_ext + ".py"

print("************ Moving code to sub-dir and generating requirement.txt to that dir ************")
replay_dir = base_dir + sub_dir + 'regen-' + curtime + '/'
os.mkdir(replay_dir)
shutil.copyfile(code_pathnm, replay_dir + file_name_wo_ext + ".py")
print(f'copied from {code_pathnm} to replay_dir + file_name_wo_ext + ".py"')

h = open(code_pathnm, "r")
code = h.read()
generate_requirements_file(code, replay_dir)
h.close()

print("************ Removing any existing Docker microservice images ************")
remove_old_image(f"generate-{service_name}")

print("************ Setting up containers using Docker Compose ************")
try:
    output1 = subprocess.run(["docker-compose", "up", "--build", "-d"], capture_output=True, text=True)
except Exception as e:
    print("************ Exception when executing setting up Docker containers ************ ")
    print("exception = ", e)
# print("Executing this process produced the following error messages:\n", output1.stderr)
#
# (ii-B)  test that all the services are started
loopnum = 0
upAndRunnning = False
while loopnum < 2 and not upAndRunnning:
    # Example usage (assuming 'docker' library is installed)
    container_name = "/generate-" + state["service_name"] + "-1"
    if is_container_running(container_name):
        upAndRunnning = True
    else:
        print(f"Container '{container_name}' is not running")
    loopnum = loopnum + 1
    time.sleep(1)   # sleep for 1 second to give time for container to start
