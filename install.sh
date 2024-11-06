#! /bin/bash

mkdir -p ~/.cshell/
rsync -r ./. --exclude .gitignore --exclude .git --exclude .gitattributes --exclude README.md --exclude misc ~/.cshell/
grep -qxF 'export PATH=PATH:"~/.cshell/cshell"' ~/.bashrc || echo 'export PATH=$PATH:~/.cshell/bin' >> ~/.bashrc
