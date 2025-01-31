@echo off

 echo ======================================================
 set DOCKER_IMAGE=tensorflow-2.10.1

if defined VIRTUAL_ENV (
    echo Virtual environment is activated.
    echo ======================================================

    rem Checking if nvidia-smi command is present
    where nvidia-smi >nul 2>nul
    if %errorlevel% equ 0 (
        echo Nvidia GPU is available.
        echo ======================================================

        rem Checking if tensorflow gpu image is present
        docker images %DOCKER_IMAGE% >nul 2>nul
        if %errorlevel% equ 0 (
            echo Tensorflow GPU image is present.
            echo ======================================================
            echo starting the web server....
             %VIRTUAL_ENV%\Scripts\python.exe ./webui/app.py

        ) else (
            echo Tensorflow GPU image is not present.
            echo Building the image.....
            docker build -t tensorflow-2.10.1  --target tfgpu -f tensorflow.dockerfile .
            echo ======================================================
            echo starting the web server....
             %VIRTUAL_ENV%\Scripts\python.exe ./webui/app.pypython3 ./webui/app.py
            
        )
        

    ) else (
        echo Nvidia GPU is not available.
        echo ======================================================

        rem Checking if tensorflow cpu image is present
        docker images %DOCKER_IMAGE% >nul 2>nul
        if %errorlevel% equ 0 (
            echo Tensorflow CPU image is present.
            echo ======================================================
            echo starting the web server....
             %VIRTUAL_ENV%\Scripts\python.exe ./webui/app.py
        ) else (
            echo Tensorflow CPU image is not present.
            echo Building the image.....
            docker build -t tensorflow-2.10.1  --target tfcpu -f tensorflow.dockerfile .
            echo ======================================================
            echo starting the web server....
             %VIRTUAL_ENV%\Scripts\python.exe ./webui/app.py
            
        )

    )

    

) else (
    echo Virtual environment is not activated.
    exit
)