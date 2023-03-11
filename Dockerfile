FROM ros:melodic

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -qqy x11-apps xfce4 novnc net-tools tigervnc-standalone-server tigervnc-xorg-extension

RUN apt-get install -qqy firefox python-pip vim wget gpg htop tree && python -m pip install opencv-python==4.2.0.32

RUN mkdir -p ~/.vnc && echo "#!/bin/bash\nstartxfce4" > ~/.vnc/xstartup && chmod +x ~/.vnc/xstartup

ADD entrypoint.sh /

RUN chmod +x /entrypoint.sh 

CMD /entrypoint.sh
