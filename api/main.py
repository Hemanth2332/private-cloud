from flask import (
    Flask,
    request
)

from dockermanager import DockerManager
from misc import Misc

app = Flask(__name__)
df = DockerManager()

@app.route("/listimages", methods=['GET'])
def home():
    return df.list_images()


@app.route("/start", methods=['POST'])
def start_containers():
    data = request.get_json()
    base_image = data['base_image']
    password = data["password"]
    hardware = data['hardware']
    ports = data['ports']

    image_name = base_image.split(":")[0] + '-image'

    if Misc.write_dockerfile(base_image=base_image, password=password, ports=ports):
        _ = df.build_image(image_name)
        container = df.start_container_with_ports(image_name,ports, gpu=True if hardware.lower() == "gpu" else False)

        return container
    

@app.route("/stop", methods=["POST"])
def stop():
    data = request.get_json()
    container_id = data['container_id']
    status = df.stop_and_remove_container(container_id)

    return status

@app.route("/listinstances", methods=['GET'])
def listinstances():
    return df.list_containers()


if __name__ == "__main__":
    app.run(host="0.0.0.0")

