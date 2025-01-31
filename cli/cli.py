import dockerfunctions as df
import writedockerfile as wf


if __name__ == "__main__":


    print("\nWelcome to the cli cloud")
    print("\n1) create a new instance")
    print("\n2) create a new instance with additional ports")
    print("\n3) list instances")
    print("\n4) stop instance")
    print("\n5) start instance")
    print("\n6) terminate instance")
    print("\n7) exit")
    print()

    while True:
        num = int(input("> "))

        if num == 1:
            print("\n Creating a instance\n")
            print()
            base_image_name = input("enter the base image: ")
            image_name = input("enter image name: ")
            passwd = input("enter the password: ")
            if wf.writedockerfile(base_image_name, passwd):
                image_name = df.build_image(image_name)
                container_id = df.start_container_with_port(image_name[0])
                print()
            else:
                print("could not create a instance")
                break

        elif num == 2:
            print("\nCreating a new instance with n ports\n")

            base_image_name = input("enter the base image: ")
            image_name = input("enter image name: ")
            passwd = input("enter the password: ")
            docker_ports = input("enter the ports [space between]: ").split(' ')

            if wf.write_docker_file_with_nos_ports(base_image_name, passwd, docker_ports):
                image_name = df.build_image(image_name)
                container_id = df.start_container_with_nport(image_name[0], docker_ports)
                print()
            else:
                print("could not create a instance")
        
        
        elif num == 3:
            print("Listing instances: \n")
            df.list_container()

        elif num == 4:
            print("\nStopping instance\n")
            _containerid = input("enter the container id (short_id): ")
            df.stop_container(_containerid)
            print()
        
        elif num == 5:
            print("\nStarting instance\n")
            _containerid = input("enter the container id (short id): ")
            df.start_container(_containerid)

        elif num == 6:
            print("\n Remove the instance (terminate)\n")
            _containerid = input("enter the container id: ").strip()
            if _containerid != "":
                df.stop_remove_container(_containerid)
            else:
                print("No id is given")
        
        elif num == 7:
            print("Exiting.....")
            break
            
    exit()


        
