from flask import Flask, render_template, request
import docker


app =Flask(__name__)

@app.route("/", methods=['GET'])
def list_images():
    client = docker.from_env()

    client = docker.from_env()

    images = client.images.list()
    image_names = []
    for i in images:
        if i.tags and "image" not in i.tags[0]:
            image_names.append(i.tags[0]) 

    
    return render_template('index.html', image_names = image_names)

@app.route("/start/<image_name>")
def start(image_name:str):
    return render_template("starter.html", image_name=image_name)

@app.route("/create", methods=['POST'])
def create():
    base_image = request.form.get("base_image")
    passwd = request.form.get("password")
    hardware = request.form.get("hardware")
    defined_ports = request.form.get("defined_ports")

    image_name = base_image.split(':')[0] + '-image'

    _ = 

if __name__ == "__main__":
    app.run()
    

    

