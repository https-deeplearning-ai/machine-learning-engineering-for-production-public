# Mac M1 setup

Some learners in a our Discourse community have found a method to get this lab running in Macs that use the M1 chip.

**Notice that this only works for `Method 1 Creating a virtual Environment` and not for the Docker method.**

If this method stops working please raise an issue to let us know!

----
## Install Tensorflow

Install TF dependencies:

`conda install -c apple tensorflow-deps`


Install TF for mac:

`python -m pip install tensorflow-macos`

Install TF Metal plugin:

`python -m pip install tensorflow-metal`

-------
## Install OpenCV

Add conda-forge to your list of channels (in this context channels are where libraries are pulled from):

`conda config --add channels conda-forge`

Install OpenCV:

`conda install -c conda-forge opencv===4.5.3`

Check your OpenCV installation:

`python -c "import cv2; print(cv2.__version__)" `

This command should print `4.5.3` in your terminal.

## Modifying requirements.txt

Since you have already installed versions of Tensorflow and OpenCV that are compatible with your mac you need to prevent these from getting modified in the next step.

To do this, open the `requirements.txt` and comment-out or delete the lines:

```txt
opencv-python-headless==4.5.3.56
tensorflow==2.7.0
```

Now you can go back to the previous [documentation](./README.md) to finish the setup!

