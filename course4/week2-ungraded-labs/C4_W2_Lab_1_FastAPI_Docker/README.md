# Week 2 Ungraded Lab: Deploy a ML model with fastAPI and Docker

Welcome! During this ungraded lab you will deploy a webserver that hosts a predictive model trained on the [wine dataset](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_wine.html#sklearn.datasets.load_wine) using [FastApi](https://fastapi.tiangolo.com/) and [Docker](https://www.docker.com/).

During Course 1 of this specialization you saw how to leverage FastAPI's webserver functionalities to deploy a Deep Learning model that detected objects in pictures. In this lab you are going to build upon that experience and integrate your code with Docker so it is portable and can be deployed with more ease.

Notice that in this lab you are going to use a simpler classifier that consists of a [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) and a [Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) with a forest of 10 trees. This classifier is the same that you used on Course 3 during the `Permutation Feature Importance` lab. This is done to avoid using libraries such as Tensorflow that will yield much longer build times when building the Docker image due to their size.


If you are a Windows user remember to use a WSL2 shell. To open such shell use the Windows search bar and type either `wsl` or `bash`, one of these should be available if you installed WSL2 previously.

Open your terminal and let's get started!

----
## Why not use Tensorflow Serving?

Not all the models you will be working with are going to be written in Tensorflow, they might not even be Deep Learning models. TFS is a great option when working with Tensorflow but more often than not you will need the extra flexibility that comes with coding the webserver yourself.

Along with this, it is a great learning experience to better understand how web servers integrate with classifiers to deploy ML algorithms.

----


## How this lab works


By the end of this lab you will have built two versions of the webserver, one that can output only one prediction per request and another one that enables batching. During this you will learn about some of FastAPI's features, how to create a `Dockerfile` and other key Docker concepts such as `image tagging`.

The best way to follow along is to read this documentation from your browser while working on a cloned version of this repo on your local machine by using a terminal.

Within the documentation, snippets of the files will be displayed with a description of what is going on. Notice that the same code can be found within the repo.

To clone this repo use the following command:

```bash
git clone https://github.com/https-deeplearning-ai/machine-learning-engineering-for-production-public.git
```

or for cloning via SSH use:

```bash
git clone git@github.com:https-deeplearning-ai/machine-learning-engineering-for-production-public.git
```

--------

Let's get started by jumping to the section [Part 1 - One prediction per request](./no-batch/README.md)!

Or if you have already completed part 1 you can jump straight to [Part 2 - Adding batching to the server](./with-batch/README.md)!
