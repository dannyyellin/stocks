import docker

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


def list_containers():
    print("list containers:")
    client = docker.from_env()
    if client.containers.list() == []:
        print("no containers in containers.list")
        return
    else:
        for c in client.containers.list():
            # print(f"container attrs are {container.attrs}")
            Name = c.attrs.get('Name')
            Status = c.attrs.get('State')['Status']
            # Port = container.attrs.get('NetworkSettings')['Ports']
            print(f"Container {Name} has Status {Status}")
            return


def remove_container(container_name):
    print("remove_container: container_name= ", container_name)
    client = docker.from_env()
    try:
        for container in client.containers.list():
            name = container.attrs.get("Name")
            if container_name == name:
                container.kill()
                return
    except docker.errors.NotFound:
        print(f"No container named {container_name} found")
    except Exception as e:
        print("remove_container: exception raised:", str(e))


def remove_all_containers():
    client = docker.from_env()
    try:
        for c in client.containers.list():
            c.kill()
    except Exception as e:
        print("remove_all_containers: exception raised:", str(e))


def list_images():
    print("list images:")
    client = docker.from_env()
    if client.images.list() == []:
        print("no images in images.list")
        return
    else:
        for i in client.images.list():
            # print(f"container attrs are {container.attrs}")
            Name = i.attrs.get('Name')
            ID = i.id
            tags = i.tags
            print(f"Image {Name} has ID {ID} and tags {tags}")
            return


def remove_image(image_name):
    client = docker.from_env()
    print("remove_image:")
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

