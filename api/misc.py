import os
import socket


class Misc:
    @staticmethod
    def get_ip_address() -> str:
        """Returns the IP address of the host machine."""
        try:
            return socket.gethostbyname(socket.gethostname())
        except socket.error:
            return ""

    @staticmethod
    def generate_dockerfile_contents(base_image: str, password: str, ports: list = None) -> str:
        """Generates the contents of a Dockerfile."""
        if ports is None:
            ports = []
        
        expose_ports = "EXPOSE 22 " + " ".join(map(str, ports)) if ports else "EXPOSE 22"
        
        return f"""
        FROM {base_image}

        RUN apt-get update && \
            apt-get install -y openssh-server && \
            apt-get clean && \
            rm -rf /var/lib/apt/lists/*

        RUN mkdir -p /var/run/sshd
        RUN echo 'root:{password}' | chpasswd
        RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

        {expose_ports}

        CMD ["/usr/sbin/sshd", "-D"]
        """

    @staticmethod
    def write_dockerfile(base_image: str, password: str, ports: list = None) -> bool:
        """Writes the generated Dockerfile contents to a file."""
        if ports is None:
            ports = []
        
        contents = Misc.generate_dockerfile_contents(base_image, password, ports)
        dockerfile_path = "./dockercontext/Dockerfile"
        os.makedirs(os.path.dirname(dockerfile_path), exist_ok=True)
        
        try:
            with open(dockerfile_path, "w") as f:
                f.write(contents)
            return True
        except OSError:
            return False
