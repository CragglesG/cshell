#! /bin/bash

mkdir -p ~/.cshell/
rsync -r ./. --exclude .git ~/.cshell/
grep -qxF 'export PATH=PATH:"~/.cshell/cshell"' ~/.bashrc || echo 'export PATH=PATH:"~/.cshell/cshell"' >> ~/.bashrc
