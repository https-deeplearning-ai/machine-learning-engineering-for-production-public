# Ungraded Lab - Deploy a Deep Learning model
 
## Introduction
Welcome to the first week of Machine Learning Engineering for Production Course 1. During this ungraded lab you will get experience on how to deploy an already trained Deep Learning model through a REST API using the library fastAPI.
 
This tutorial will show you how to set up everything you need to run this lab locally. This can be done via 2 methods, using `Docker` or using `Python Virtual Environments`. 
 
Both should yield the same result so if you already have conda installed we recommend you use the virtual environments method, if not, the Docker method is probably easier to set up.
 
The commands on this tutorial are meant to be run within a terminal. Before going forward **clone this repo in your local filesystem and `cd` to the week1-ungraded-lab directory**.

To clone the repo use this command:
```bash
git clone https://github.com/https-deeplearning-ai/MLEP-public.git
```

Or if you prefer SSH, use this one:
```bash
git clone git@github.com:https-deeplearning-ai/MLEP-public.git
```

To change directories into the appropriate one, you need to be in the directory where you cloned the repo and use:
```bash
cd MLEP-public/week1-ungraded-lab
```

Once in the `week1-ungraded-lab` directory you can see the files in it using the `ls` command.
Let's take a quick look at them:
 
```
.
└── Root of repo/
    └── week1-ungraded-lab (this directory)
        ├── images (includes some images from ImageNet)
        ├── server.ipynb (Part 1 of the ungraded lab)
        ├── client.ipynb (Part 2 of the ungraded lab)
        └── requirements.txt (python dependencies)
```
 
 
## Method 1: Python Virtual Environments with Conda
 
### Prerequisites: Have [conda](https://docs.conda.io/en/latest/) installed on your local machine.
 
You will use Conda as an environment management system so that all the dependencies you need for this ungraded lab are stored in an isolated environment.
 
Conda includes a lot of libraries so if you are only installing it to complete this lab (and can't or won't use the Docker method), we suggest you check out [miniconda](https://docs.conda.io/en/latest/miniconda.html), which is a minimal version of conda.
 
### 1. Create a virtual Environment
 
Once you have Conda installed and configured to be run on a shell or terminal (if you are on Windows you might need to use the Anaconda Prompt), create a new developing environment with python 3.7 using the following command:
 
```bash
conda create --name deploy-lab-env python=3.7
```
 
In case you're wondering, `ugl` stands for "ungraded lab". After it is successfully created, activate it like this:
 
```bash
conda activate deploy-lab-env
```
 
Now all of the libraries you install will be isolated to this environment. 
 
### 2. Install dependencies using PIP 
 
Double check that you are currently on the `week1-ungraded-lab` directory, which includes the `requirements.txt` file. This file lists all required dependencies and their respective versions. Now use the following command:
 
```bash
pip install -r requirements.txt
```
 
This can take a while depending on the speed of your internet connection. When this is done you should be ready to spin up jupyter lab and begin the ungraded lab.
 
### 3. Launch Jupyter Lab
 
Jupyter lab was installed during the previous step so you can launch it with this command:
```bash
jupyter lab
```
You will see some information printed in the terminal. Usually you will need to authenticate to use Jupyter lab, for this, copy the token that appears on your terminal, head over to [http://localhost:8888/](http://localhost:8888/) and paste it there.
 
### 4. Run the notebook
 
Within Jupyter lab you should be in the same directory where you used the `jupyter lab` command.
 
Look for the `server.ipynb` file and open it to begin the ungraded lab.

To stop jupyter lab once you are done with the lab just press `Ctrl + C` twice.
 
And... that's it! Have fun deploying a Deep Learning model! :)

 
# 
#
# Method 2: Docker
 
### Prerequisites: Have Docker installed on your local machine.
 
[Docker](https://www.docker.com/) is a tool that allows you to ship your software along with all the dependencies that it needs to run. You can download the free version [here](https://www.docker.com/products/docker-desktop). 
 
 
### 1. Pull the image from Docker hub

Images are an important concept within the Docker ecosystem. You can think of them as the compilation of all the elements (libraries, files, etc) needed for your software to run. 

By using the following command you will download or pull the image necessary to run this ungraded lab locally:
```bash
docker pull deeplearningai/mlepc1w1-ugl:jupyternb
```

 
### 2. Run a container out of the image:

Images can also be thought of as the blueprints for containers, which are the actual instances of the software running. To run a container using the image you just pulled, double check that you are currently on the `week1-ungraded-lab` directory and use this command:
```bash
docker run -it --rm -p 8888:8888 -p 8000:8000 --mount type=bind,source=$(pwd),target=/home/jovyan/work deeplearningai/mlepc1w1-ugl:jupyternb
```
 
Let's break down this command and its flags:
 
- -it: Runs the container in an interactive mode and attaches a pseudo-terminal to it so you can check what is being printed in the standard streams of the container. This is very important since you will have to **copy and paste the access token for Jupyter lab**.

- --rm: Deletes the container after stopping it.
- -p: Allows you to map a port in your computer to a port in the container. In this case we need a port for the Jupyter server and another for the server you will run within the ungraded lab.
- --mount: Allows you to mount a directory in your local filesystem within the container. This is very important because if no mounts are present, changes to files will not persist after the container is deleted. In this case we are mounting the current directory `week1-ungraded-lab` onto the `/home/jovyan/work` directory inside the container.
 
When the container starts running you will see some information being printed in the terminal. Usually you will need to authenticate to use Jupyter lab, for this copy the token that appears on your terminal, head over to [http://localhost:8888/](http://localhost:8888/) and paste it there.
 
Once authenticated click in the `/work` directory and you should see all of the files from your current local directory. Look for the `server.ipynb` file and open it to begin the ungraded lab.

To stop the container once you are done with the lab just press `Ctrl + C` twice. This will also delete the container.
 
And, that's it! Have fun deploying a Deep Learning model! :)
