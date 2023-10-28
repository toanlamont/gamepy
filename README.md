# Tank Game made by pygame
# 1.Installation
``````
pip install -r requirements.txt
``````
```
python3 main.py
```

# 2. Build game to android app
**Prepare environment**
```
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 Cython==0.29.33
```
**Build to apk app**
```
 buildozer android debug
```
**Deploy to android device and debug**
```
buildozer -v android debug deploy run logcat | grep 'python'
```