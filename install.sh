#! /bin/bash

mkdir -p ~/.cshell/
rsync -r ./. --exclude .git ~/.cshell/