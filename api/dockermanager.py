import docker
import random
from typing import List, Optional, Dict


class DockerManager:
    def __init__(self):
        self.client = docker.from_env()


    def _get_container(self, container_id: str):
        """Fetches a container by ID."""
        try:
            return self.client.containers.get(container_id)
        except docker.errors.NotFound:
            print(f"Container {container_id} not found.")
        except docker.errors.APIError as e:
            print(f"Docker API error: {e}")
        return None
    
    def list_containers(self):
        containers = self.client.containers.list()
        img = []
        for i in containers:
            mycontainer = {}
            mycontainer['container_id'] = i.short_id
            mycontainer['name'] = i.name
            mycontainer['status'] = i.status
            mycontainer['ports'] = {port: details[0].get('HostPort') for port, details in i.ports.items()}
            mycontainer['image'] = i.image.tags[0] if i.image.tags else i.image.id
            img.append(mycontainer)

        return {"containers_running": img}
    

    def list_images(self) -> List[str]:
        """List all the Docker images available."""
        image_names = [i.tags[0] for i in self.client.images.list() if i.tags and "image" not in i.tags[0]]
        return {"images_present": image_names}
    

    def build_image(self, image_name: str, path: str = "dockercontext") -> Optional[List[str]]:
        """Builds a Docker image from the specified path."""
        try:
            image, _ = self.client.images.build(path=path, tag=image_name)
            return image.tags
        except (docker.errors.BuildError, docker.errors.APIError) as e:
            print(f"Failed to build image: {e}")
            return None


    def start_container(self, container_id: str) -> Dict:
        """Starts a container by ID."""
        container = self.get_container(container_id)
        if container:
            try:
                container.start()
                return {"container_id": container.short_id, "contianer_status": "running"}
            except docker.errors.APIError as e:
                return {"error":f"Failed to start container {container_id}: {e}"}


    def start_container_with_ports(self, image_name: str, ports: List[str] = None, gpu: bool = False) -> Optional[dict]:
        """Starts a container with specified ports and optional GPU support."""
        ports_open = ['22']
        if ports:
            ports_open.extend(ports)
        
        port_maps = {port: random.randint(10000, 65535) for port in ports_open}
        device_requests = [docker.types.DeviceRequest(device_ids=["0"], capabilities=[["gpu"]])] if gpu else []
        
        try:
            container = self.client.containers.run(
                image_name,
                detach=True,
                ports=port_maps,
                device_requests=device_requests
            )
            
            return {"image_name":image_name ,"container_id":container.short_id, "port_maps":port_maps}
        except docker.errors.APIError as e:
            return {"error": f"Could not start the container: {e}"}


    def stop_container(self, container_id: str) -> bool:
        """Stops a container by ID."""
        container = self.get_container(container_id)
        if container:
            try:
                container.stop()

                return {"container":container_id, "status": "stopped"}
            except docker.errors.APIError as e:
                return {"error":f"Failed to stop container {container_id}: {e}"}


    def stop_and_remove_container(self, container_id: str) -> Dict:
        """Stops and removes a container by ID."""
        container = self._get_container(container_id)
        if container:
            try:
                container.stop()
                container.remove()

                return {"container": container_id, "status": "removed"}
            except docker.errors.APIError as e:
                return {"error":f"Error removing container {container_id}: {e}"}
