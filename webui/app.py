from flask import (
    Flask,
    render_template,
    request,
    redirect
)
import subprocess
import docker
import socket
import api_dockerfunctions as df
import api_writedockerfile as wf

def check_gpu_existence():
    try:
        result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:
        return False
    

def get_ipaddress():
    try:
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        return ip_addr
    except socket.error as e:
        return None


app = Flask(__name__)

IP_ADDR = get_ipaddress()

IMG_LIST = [
          {"name":"Python", "filepath":"python.jpeg"},
          {"name":"Debian", "filepath":"debian.jpeg"},
          {"name":"Ubuntu", "filepath":"ubuntu.jpeg"},
          ]



@app.route("/", methods=['GET'])
def getindex():
    return render_template("index.html", images=IMG_LIST)


@app.route("/start/<image_name>")
def start_instance(image_name:str):
    return render_template("starter.html", img_name=image_name)


@app.route("/listinstance")
def list_instance():
    client = docker.from_env()
    containers = client.containers.list()
    img = []
    for i in containers:
        mycontainer = {}
        mycontainer['container_id'] = i.short_id
        mycontainer['name'] = i.name
        mycontainer['status'] = i.status
        mycontainer['ports'] = {port: details[0].get('HostPort') for port, details in i.ports.items()}
        mycontainer['image'] = i.image.tags[0] if i.image.tags else i.image.id
        img.append(mycontainer)
    
    return render_template("list_instances.html", images=img , ip_addr = IP_ADDR)


@app.route("/create", methods=['POST'])
def test():

    base_image = request.form.get("base_image")
    passwd = request.form.get("password")
    hardware = request.form.get("hardware")
    defined_ports = request.form.get("defined_ports")
        
    img_list = ['debian-image', 'ubuntu-image', 'python-image', 'tensorflow-image']
    mydict = {v.split('-')[0]:v for v in img_list}
    image_name = mydict[base_image.split(":")[0]]
    

    if hardware == "GPU":
        if len(defined_ports) == 0:

            try:
                if wf.writedockerfile(request.form.get("base_image"), passwd):
                    image_name = df.build_image(image_name)
                    container_id = df.start_container_with_port(image_name[0], gpu=True)
                    return redirect("/listinstance")
                
            except Exception as e:
                return "could not start an instance" + str(e)

        else:
            mul_ports = defined_ports.split(",")
            print(mul_ports)
            if wf.write_docker_file_with_nos_ports(base_image_name=base_image, passwd=passwd, ports=mul_ports):
                img = df.build_image(image_name)
                _ = df.start_container_with_nport(img[0], mul_ports, gpu=True)
                return redirect("/listinstance")
            
    else:
        if len(defined_ports) == 0:

            try:
                if wf.writedockerfile(request.form.get("base_image"), passwd):
                    img = df.build_image(image_name)
                    _ = df.start_container_with_port(img[0])
                    return redirect("/listinstance")
                
            except Exception as e:
                return "could not start an instance" + str(e)

        else:
            mul_ports = defined_ports.split(",")
            print(mul_ports)
            if wf.write_docker_file_with_nos_ports(base_image_name=base_image, passwd=passwd, ports=mul_ports):
                img = df.build_image(image_name)
                _ = df.start_container_with_nport(img[0], mul_ports)
                return redirect("/listinstance")
    


@app.route("/stopinstance/<image_name>")
def stopinstance(image_name:str):
    try:
        df.stop_remove_container(image_name)
        return redirect("/listinstance")

    except Exception as e:
        return "could not stop the container " + str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
