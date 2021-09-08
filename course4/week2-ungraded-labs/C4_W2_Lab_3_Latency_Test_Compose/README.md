# Week 2 Ungraded Lab: Load testing servers with Docker Compose and Locust

Welcome! During this ungraded lab you will be conducting a load test on the servers you coded in a previous ungraded lab (first one of this week). You will compare latency across four servers:
- The server that didn't support batching
- The one with batching and using:
    -  batches of 1 
    -  batches of 32
    -  batches of 64

Technically there are only two servers (the one with and the one without batching) but you will for sake of practicality consider them as separate ones since they will handle different amounts of data.

You will do this by using [Locust](https://locust.io/) which is a great Open Source load testing tool and [Docker Compose](https://docs.docker.com/compose/) which allows you to run multiple-container applications.

You will spin a total of 5 containers, 4 for each one of the servers previously mentioned and 1 that will run Locust so you don't have to install it. Before going forward, open a terminal window and run the following command to download the Locust image, this will take some minutes so it is better to do it right away:

```bash
docker pull locustio/locust
```

You should also have the images `mlepc4w2-ugl:no-batch` and `mlepc4w2-ugl:with-batch` which you built during the previous lab. **Before going forward make sure you have these two images as well as the `locustio/locust:latest` one**. You can double check using the `docker images` command. 

Open a terminal and `cd` into the directory that contains the files needed by this lab. Assuming you are on the root of the repo you can use the command `cd course4/week2-ungraded-labs/C4_W2_Lab_3_Latency_Test_Compose`.


Let's get started!

-----

## Why and how to use Docker Compose

You could manually spin up the 5 containers but you will need to find a way to link them together via a network. This can be achieved using regular Docker commands but it is much easier to accomplish using Docker Compose. 

Instead of running each container in a separate terminal window you can simply define a configuration file in `YAML` format and use the `docker-compose up` command to run your multi-container application. In case you haven't worked with `YAML` files, these are usually for configuration and they work in a similar fashion to Python, by using indentation to specify scope.

Let's take a look at the beggining of `docker-compose.yml` file:
```yml
version: "3.9"
services:
  no-batch:
    image: mlepc4w2-ugl:no-batch
    links:
      - locust
```

The first line specifies the version of Compose format being used. At the time this tutorial is written the latest version is 3.9, so that is the format selected. Notice that latter versions of Compose do not require this to be explicitly stated but it is something quite common so it is worth understanding its meaning.

After this you will define each one of your `services` (or containers). You will specify the name of the service (`no-batch` in this case) along with the necessary information to run it. In this case, this is the server that does not support batching so a container that uses the image `mlepc4w2-ugl:no-batch` must be used. Notice the `links` item, this is used to tell Compose that this service will need to communicate with the service named `locust` through the network that Compose will create. 

To better understand this, look at the complete `docker-compose.yml` file:
```yml
version: "3.9"
services:
  no-batch:
    image: mlepc4w2-ugl:no-batch
    links:
      - locust
  batch-1:
    image: mlepc4w2-ugl:with-batch
    links:
      - locust
  batch-32:
    image: mlepc4w2-ugl:with-batch
    links:
      - locust
  batch-64:
    image: mlepc4w2-ugl:with-batch
    links:
      - locust
  locust:
    image: locustio/locust
    ports:
      - "8089:8089"
    volumes:
      - ./:/mnt/locust
    command: -f /mnt/locust/locustfile.py
```

Each one of the four servers that handle predictions need to be linked to the locust service so that you can perform the load test. Notice that the the servers that support batching have identical information except for the name of the service. 

The locust service has some more stuff going on but at this point you have already seen how they work:

- First, this container will have port 8089 mapped to port 8089 in your localhost. This is for you to be able to access the service directly. 

- There is also a volume, this is very similar to the bind mounts you saw in previous labs. This allows you to mount files in your local filesystem onto the container, it is often used to persist changes but in this case it is done so you don't have to create a new image that uses the `locustio/locust` one as base and copies the `locustfile.py` inside the image. 

- Finally the `command` item is analogous to the `CMD` instruction and it refers to the command that will be run when spinning up the container, in this case the locust server is started to perform the load testing.

Before spinning up this multi-container application, let's take some time to understand how `locust` works at a high level.

## Understanding Locust

By convention the file that handles the locust logic is named `locustfile.py`. Unlike Dockerfiles, this file is a regular python script. Remember you can take a look at the complete file in this repo.

The way locust works is by simulating users that will constantly send requests to your services. By doing this you can measure things like `RPS` (requests per second) or the average time each request is taking. **This is great to understand the limitations of your servers and to test if they will work under the circumstances they will be exposed once they are launched into production.**

Using locust is actually quite straightforward. First you need to create a new class that inherits from `locust.HttpUser` and within this class you need to specify a method for every service you want to test. These functions should be decorated with the `locust.task` decorator. 

Take a look at how this looks:

```python
class LoadTest(HttpUser):
    wait_time = constant(0)
    host = "http://localhost"

    @task
    def predict_batch_1(self):
        request_body = {"batches": [[1.0 for i in range(13)]]}
        self.client.post(
            "http://batch-1:80/predict", json=request_body, name="batch-1"
        )
```

Notice the two variables `wait_time` and `host`, let's quickly clarify those: 

- `wait_time` tells locust how much time to wait between each request, in this case you want it to send requests as soon as possible to see how the servers perform under extreme conditions. The constant function is actually `locust.constant`.

- `host` specify the host where the service you are testing is hosted. Locust is usually meant to test several endpoints within the same host, but in this case we are testing four different servers located on four different hosts. In this case `host` defaults to 
`http://localhost` but you will actually specify each host within the task functions so this parameter actually does nothing but it is required by locust so you need to specify some value.

Now let's understand the task method to test the server that will handle batches of 1 data point. This is a method of the `LoadTest` class so it must have `self` as a parameter. 

In this case you are not interested in the actual predictions of the server so you will define a generic batch of data containing only 1's. Use this list of lists (which is what the server expects) to create a dictionary and pass it as `JSON` when doing the `POST` request. The request is done by using the `self.client.post` function. Notice the URL that is passed to this function, it is `http://batch-1:80/predict`. 

Remember that all of the servers listen on port `80` of their respective containers and the model is hosted on the `/predict` endpoint. **Something very important is the hostname used, in this case it is `batch-1`, which is what you named the service that will handle batches of 1 in the `docker-compose.yml` file.**

The methods to test the other servers are nearly identical to this one, except for the URL used and the data passed to the request. Take a look at the complete `locustfile.py`:


```python
from locust import HttpUser, task, constant


class LoadTest(HttpUser):
    wait_time = constant(0)
    host = "http://localhost"

    @task
    def predict_batch_1(self):
        request_body = {"batches": [[1.0 for i in range(13)]]}
        self.client.post(
            "http://batch-1:80/predict", json=request_body, name="batch-1"
        )

    @task
    def predict_batch_32(self):
        request_body = {"batches": [[1.0 for i in range(13)] for i in range(32)]}
        self.client.post(
            "http://batch-32:80/predict", json=request_body, name="batch-32"
        )

    @task
    def predict_batch_64(self):
        request_body = {"batches": [[1.0 for i in range(13)] for i in range(64)]}
        self.client.post(
            "http://batch-64:80/predict", json=request_body, name="batch-64"
        )

    @task
    def predict_no_batch(self):
        request_body = {
            "alcohol": 1.0,
            "malic_acid": 1.0,
            "ash": 1.0,
            "alcalinity_of_ash": 1.0,
            "magnesium": 1.0,
            "total_phenols": 1.0,
            "flavanoids": 1.0,
            "nonflavanoid_phenols": 1.0,
            "proanthocyanins": 1.0,
            "color_intensity": 1.0,
            "hue": 1.0,
            "od280_od315_of_diluted_wines": 1.0,
            "proline": 1.0,
        }
        self.client.post(
            "http://no-batch:80/predict", json=request_body, name="0:batch"
        )
```


Now that you understand how locust works it is finally time to perform load testing on your servers!

## Load Testing the servers

Be sure that you are in the same directory as the `locustfile.py` and `docker-compose.yml` files and run the following command:

```bash
docker-compose up
```

Docker Compose will automatically spin up all of your services and create a network for them to communicate. Isn't that neat?

Now head over to [http://localhost:8089/](http://localhost:8089/) and you will see locust's interface. Here you can select the amount of users you desire as well as the spawn rate (this is how many new users per second are added until reaching the total amount desired).

**Start with low values because the more users you add more memory will be required and you risk crashing the application.** A good start point is 10 Number of users and 10 Spawn rate. 

Now click on the `Start swarming` button and the load test will start. You will see a dashboard that looks like this:

![locust](../../assets/locust-home.png)

Each row corresponds to a service you are testing. You can tell which is which by looking at the name (these were defined in the `locustfile.py`). 

The first two columns show you the number of requests sent to each server and the number of those requests that failed.

The next five columns (highlighted in orange) shows some descriptive statistics about the latency of the servers in milliseconds. 

The next column (highlighted in pink) shows the average amount of bytes that is being handled by the server with each request. Notice that the larger the batches, the larger this number will be.

The next column (highlighted in blue) shows the `RPS` of each server. In this case this metric is not the most reliable since locust tries to send the same amount of traffic to each service but there is some variance in this process. Because of this it is better to take decisions based on the latency information which is agnostic to the amount of requests.

Now it is your turn to play some more with this. To stop the current test click on the `Stop` button in the upper right corner of the screen. Now you can submit new values for the Number of users and Spawn rate. You should be safe using values up to 500 so try a couple of different values and see what you get!

## Stopping the application

Once you are done with this lab go into the terminal window where you run the `docker-compose up` command and use the key combination `ctrl + c` once to stop the multi-container application. 

At this point the containers have been stopped but not removed. To remove them along with the network that was created use the `docker-compose down` command.

----
**Congratulations on finishing this ungraded lab!**

In this lab you saw how to use Docker Compose to run multiple-container applications by setting a configuration file in `YAML` format. This is a much better alternative than spinning and linking the containers manually as it handles most of this for you. You also were exposed to Locust and how it can be leveraged to perform load testing on your servers.

Now you should have a clearer understanding of how to use these tools to create production-ready services that will endure the conditions they will be exposed to once deployed to the outside world.

**Keep it up!**
