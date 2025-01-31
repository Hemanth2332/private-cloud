FROM python:3.10-slim

RUN apt-get update &&     apt-get install -y openssh-server &&     apt-get clean &&     rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

EXPOSE 22 8000 
CMD ["/usr/sbin/sshd", "-D"]