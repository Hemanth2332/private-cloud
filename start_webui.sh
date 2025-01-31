#!/bin/bash

echo "====================================================================="

if [[ $VIRTUAL_ENV ]]
then
    echo "virtual environment is activated"
    echo "======================================================================"

        if command -v nvidia-smi &> /dev/null
        then
                echo 'nvidia driver is installed'

                img_check=$(docker image ls| grep tensorflow- | awk '{ print $1 }')

                if [[ "$img_check" == "tensorflow-2.10.1" ]]
                then
                        echo "tensorflow image built exists"
                        echo "======================================================================"
                        echo "starting the web server ......."
                        python3 webui/app.py
                else
                        echo "tensorflow  is not built"
                        echo "building the GPU tensorflow image"
                        echo "--------------------------------------------------------"
                        docker build -t tensorflow-2.10.1  --target tfgpu -f tensorflow.dockerfile .
                        echo "======================================================================"
                        echo "starting the web server ......."
                        python3 webui/app.py

                fi

        

        else
                echo 'nvidia driver is not installed'

                img_check=$(docker image ls| grep tensorflow- | awk '{ print $1 }')

                if [[ "$img_check" == "tensorflow-" ]]
                then
                        echo "tensorflow image built exists"
                else
                        echo "tensorflow  is not built"
                        echo "building the CPU tensorflow image"
                        echo "--------------------------------------------------------"
                        docker build -t tensorflow-2.10.1 --target tfcpu -f tensorflow.dockerfile .
                        echo "======================================================================"
                        echo "starting the web server ......."
                        python3 webui/app.py

                fi

        fi
else
    echo "virtual environment directory is not found"
    echo "====================================================================="
    exit
fi


