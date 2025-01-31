import docker
import random
import socket

def get_ipaddress():
    try:
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        return ip_addr
    except socket.error as e:
        return None
    

def build_image(image_name:str) -> str:
    client = docker.from_env()
    try:
        image, _ = client.images.build(path="dockercontext", tag=image_name)
        
        # print(f"Image built successfully: {image.tags}")
        return image.tags

    except docker.errors.BuildError as e:
        print(f"Failed to build image: {e}")
    except docker.errors.APIError as e:
        print(f"Docker API error: {e}")


def list_container():
    client = docker.from_env()

    try:

        running_containers = client.containers.list()
        if len(running_containers) != 0:
            
            for container in running_containers:
                print(f"Container ID: {container.short_id}")
                print(f"Container Name: {container.name}")
                print(f"Image: {container.image}")
                print(f"Status: {container.status}")
                print(f"Ports: {container.ports}")
                print("------------------------------\n")
        else:
            print("No instances running\n")

    except docker.errors.APIError as e:
        print(f"Error getting running containers: {e}")


def start_container(container_id:str):
    client = docker.from_env()

    try:
        container = client.containers.get(container_id)
        container.start()
        print(f"container started: {container.short_id}")
    
    except Exception as e:
        print(f"container cannot be started {container.short_id}")


def start_container_with_port(imageName:str):
    client = docker.from_env()
    host_port = random.randint(10000,65535)
    try:
        container = client.containers.run(
            imageName, 
            detach=True, 
            ports={'22':host_port}
        )
        print(f"\ncontainer id: {container.short_id}\
              \nConnect: ssh root@localhost -p {host_port} \
(or) ssh root@{get_ipaddress()} -p {host_port}")
        return (container.short_id)

    except Exception as e:
        print("could not start the container")
        return None


def stop_container(container_id:str):
    client = docker.from_env()
    try:
        container = client.containers.get(container_id)
        container.stop()
        print(f"Container {container.short_id} stopped")

    except Exception:
        print(f"could not stop or find the container")


def stop_remove_container(container_id:str):
    client = docker.from_env()

    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()

        print(f"Container {container_id} removed successfully.")
    
    except docker.errors.NotFound as e:
        print(f"Container {container_id} not found: {e}")
    except docker.errors.APIError as e:
        print(f"Error removing container {container_id}: {e}")


def start_container_with_nport(imageName:str, ports:list):
    client = docker.from_env()

    docker_port_list = ['22']
    docker_port_list.extend(ports)
    host_port_list = [random.randint(10000, 65535) for _ in range(len(docker_port_list))]
    port_maps = {k:v for k,v in zip(docker_port_list, host_port_list)}

    try:
        container = client.containers.run(
            imageName, 
            detach=True, 
            ports=port_maps
        )
        print(f"\ncontainer id: {container.short_id}\
    \nConnect: ssh root@localhost -p {port_maps['22']} \
    (or) ssh root@{get_ipaddress()} -p {port_maps['22']}")
        
        print("port mappings:\n {}".format(port_maps))
        return (container.short_id)

    except Exception as e:
        print("could not start the container ", e)
        return None
