Super Yurrei no Jikaru III
==========================

![](./cover/cover.png)

Installation
------------

- Pygame (for Python3)

Instructions taken from [this thread](http://askubuntu.com/questions/401342/how-to-download-pygame-in-python3-3)

```
# Change to your home directory.
cd ~

# Get Pygame source code.
sudo apt-get install mercurial
hg clone https://bitbucket.org/pygame/pygame
cd pygame

# Install dependencies.
sudo apt-get install python3-dev python3-numpy libsdl-dev libsdl-image1.2-dev \
  libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev \
  libavformat-dev libswscale-dev libjpeg-dev libfreetype6-dev python3-setuptools

# Build and install Pygame.
python3 setup.py build
sudo python3 setup.py install
```

- Python Image Library (PIL) (for Python 3)

```
sudo apt-get install python3-pip
sudo pip3 install Pillow
```

Play
----

```
# Go to the game directory
cd superYurreiNoJikaruIII

# Launch it
./play
```

