FROM ubuntu:trusty
# derived from https://registry.hub.docker.com/u/ksoichiro/pandoc/
# http://www.unexpected-vortices.com/doc-notes/markdown-and-rest-compared.html
# https://github.com/embolalia/Sphinx-Pandoc
# https://github.com/mctenshi/sphinx-markdown-sample
MAINTAINER Chuck Butler "chuck.butler@canonical.com"

RUN mkdir /opt
RUN apt-get update -qq
RUN apt-get upgrade -qq

ENV HOME /root
RUN apt-get install -y -qq texlive
RUN apt-get install -y -qq haskell-platform

RUN apt-get install -y -qq python3-pip \
                           git \
                           python-sphinx3 \
                           python-sphinxcontrib.actdiag \
                           python-sphinxcontrib.blockdiag \
                           python-sphinxcontrib.nwdiag \
                           python-sphinxcontrib.seqdiag

RUN pip3 install sphinx_bootstrap_theme
RUN git clone https://github.com/juju-solutions/sphinx-markdown-sample.git /opt/smd

RUN cabal update
RUN cabal install zip-archive
RUN cabal install pandoc pandoc-citeproc

# Cleaning
RUN apt-get clean

ENV PATH $HOME/.cabal/bin:$PATH
VOLUME /workspace
WORKDIR /workspace
