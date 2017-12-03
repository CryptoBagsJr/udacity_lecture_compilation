# udacity_lecture_compilation

# Install required software

## Install Anaconda
- http://www.continuum.io/downloads

```
$ conda upgrade Anaconda
$ conda upgrade -all
```

## Install package: numpy, scipy, pandas

```
$ conda install numpy scipy pandas
```

## Manage Environment for tensorflow
```
$ conda create -n tensorflow python=3
```

## Enter the environment
```
$ source activate tensorflow
```

## Leave the Environment
```
$ source deactivate
```

## Install Jupyter Notebook
```
$ conda install jupyter Notebook
```
or
```
$ pip install jupyter Notebook
```

## Install packages
```
# install tensorflow
$ pip install tensorflow  # CPU version
$ pip install tensorflow-gpu # GPU version

# install keras
$ pip install keras

# Install opencv
$ pip install opencv-python

# Install matplotlib
$ conda install matplotlib

# Install pillow
$ conda install pillow

# Moviepy
$ pip install Moviepy
$ pip install h5py

# ffmpeg
$ brew install ffmpeg
$ brew install pyqt
```

# Start Jupyter Notebook
```
# Enter the Environment
$ source activate tensorflow # tensorflow: environment name

$ jupyter notebook
# This will launch the browser and open a current page in notebook.
```
