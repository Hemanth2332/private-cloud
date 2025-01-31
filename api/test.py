import requests
from misc import Misc
from dockermanager import DockerManager

df = DockerManager()

BASE_URL = "http://127.0.0.1:5000"  


def test_list_images():
    response = requests.get(f"{BASE_URL}/listimages")
    print("Test /listimages:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_start_containers():
    
    test_data = {
        "base_image": "python:3.10-slim",  
        "password": "example_password",
        "hardware": "CPU",  
        "ports": ["8080", "5000"]
    }
    
    response = requests.post(
        f"{BASE_URL}/start", 
        json=test_data
    )
    print("Test /start:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_stop():
    
    test_data = {
        "container_id": "d21cea12ad7"  
    }
    
    response = requests.post(
        f"{BASE_URL}/stop", 
        json=test_data
    )
    print("Test /stop:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_list_instances():
    response = requests.get(f"{BASE_URL}/listinstances")
    print("Test /listinstances:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")


if __name__ == "__main__":
    base_image = "golang:latest"
    password = "hello"
    ports = [3000]
    hardware = "CPU"

    image_name = base_image.split(":")[0] + '-image'

    if Misc.write_dockerfile(base_image=base_image, password=password, ports=ports):
        _ = df.build_image(image_name)
        container = df.start_container_with_ports(image_name,ports, gpu=True if hardware.lower() == "gpu" else False)

        print(container)

