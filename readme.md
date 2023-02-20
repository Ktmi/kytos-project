# What Is This?

This is a quick and easy way for creating
a basic dev environment for the Kytos.

# How Do I Use It?

After cloning this project to your system, make sure that all submodules
are initialized.

```bash
git submodule init
```

Then create a python virtual environment which to install
Kytos and its NApps into.

```bash
python3 -m venv kytos-environment
```

Finally, with the virtual environment activated, run
the `install-dependencies.py` script.

```bash
source kytos-environment/bin/activate
python install-dependencies.py
```