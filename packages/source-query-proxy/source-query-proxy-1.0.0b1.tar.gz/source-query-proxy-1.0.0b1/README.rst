
source-query-proxy
==================

Credits
-------

Source Engine messages inspired by **Python-valve**
https://github.com/serverstf/python-valve

Prerequisites
-------------

Python 3.7 or above

You can use `pyenv <https://github.com/pyenv/pyenv>`_ to install any version of Python without root privileges

Installing
----------

.. code-block:: bash

    pip install source-query-proxy

Run
---

.. code-block:: bash

    sqproxy run


Run with eBPF
-------------


1. Install eBPF requirements https://github.com/spumer/source-query-proxy-kernel-module/src-ebpf/README.md

2. Download script

    .. code-block:: bash

        wget https://github.com/spumer/source-query-proxy-kernel-module/archive/v1.0.0.tar.gz -O - | tar -xzvp ./source-query-proxy-kernel-module-1.0.0/src-ebpf && mv ./source-query-proxy-kernel-module-1.0.0/src-ebpf ./src-ebpf && rmdir source-query-proxy-kernel-module-1.0.0

3. Enable eBPF in config (see examples/00-globals.yaml)

4. Run

    .. code-block:: bash

        sqproxy run


Development
-----------

.. code-block:: bash

    git clone https://github.com/spumer/source-query-proxy.git
    cd source-query-proxy
    poetry install
