#!/usr/bin/env bash

if ! [ -x /usr/bin/nproc ]; then
    echo "nproc is not installed. Please install it."
    exit 1
fi
CORES=$(nproc)
#EXAMPLE=
#mpiexec -np ${CORES} python ./hello_world${EXAMPLE}.py
mpiexec -np 7 python ./mpi.py
#mpiexec -np 16 python ./hello_world${EXAMPLE}.py
