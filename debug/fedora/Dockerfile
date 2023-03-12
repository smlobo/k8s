FROM fedora

# Update the image with the latest packages (recommended)
RUN dnf update -y; dnf clean all

RUN dnf groupinstall -y "Development Tools"

RUN dnf install -y \
	vim \
	java-1.8.0-openjdk-devel \
	ant \
	openssh-clients \
	openssl-devel \
	wget \
	git \
	mercurial \
	maven \
	golang \
	python3 \
	llvm \
	clang \
	lldb \
	net-tools \
	iputils

ENV BASH_ENV=/root/.bashrc
ENV TZ=America/New_York

# ~/.bashrc
#  +-> copy from ~/.bashrc
#  +-> add go to path
#

