def writedockerfile(base_image_name:str, passwd:str) -> bool:

    contents = f"""FROM {base_image_name}

RUN apt-get update && \
    apt-get install -y openssh-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd
RUN echo 'root:{passwd}' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Expose SSH port
EXPOSE 22

# Start SSH server
CMD ["/usr/sbin/sshd", "-D"]
"""
    
    try:
        with open('./dockercontext/Dockerfile', "w") as f:
            f.write(contents)
        return True
    except Exception:
        return False


def write_docker_file_with_nos_ports(base_image_name:str, passwd:str, ports:list) -> bool:

    contents = f"""FROM {base_image_name}

RUN apt-get update && \
    apt-get install -y openssh-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd
RUN echo 'root:{passwd}' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
"""
    
    expose_str = "EXPOSE 22 "
    for i in ports:
        expose_str += f"{i} "

    contents += f"\n{expose_str}"

    contents += '\nCMD ["/usr/sbin/sshd", "-D"]'
    
    try:
        with open('./dockercontext/Dockerfile', "w") as f:
            f.write(contents)
        return True
    except Exception:
        return False
