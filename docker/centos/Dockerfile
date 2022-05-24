FROM centos:7
ENV container docker
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
RUN yum update -y \
    &&  yum install -y openssh-server openssh-clients python3 wget \
    &&  yum clean all \
    &&  wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup \
    &&  chmod +x mariadb_repo_setup \
    &&  ./mariadb_repo_setup \
    &&  rm mariadb_repo_setup \
    &&  sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config \
    &&  echo 'root:toor' | chpasswd 
VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]