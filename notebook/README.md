To build the image required for this lab run the following command:

```bash
docker build -t mlepc1w1:nb .
```

Once built you can spin a container out of it using the command:

```bash
docker run -it --rm -p 8888:8888 -p 8000:8000 --mount type=bind,source=$(pwd),target=/home/jovyan/work mlepc1w1:nb
```

To access the jupyter notebook copy the token that appears on your terminal and go to [localhost:8888/](http://localhost:8888/). Here copy the token and you will be able to enter.

Look for the `server.ipynb` file inside the `work/` directory. Within this notebook you will spin a web server. To interact with it, visit [localhost:8000/docs](http://localhost:8000/docs).
