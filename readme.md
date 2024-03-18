# What Is This?

This is a quick and easy way for creating
a basic dev environment for the Kytos.

# What do I need?

In order to run kytos you need to install the following dependencies

 - `git`
 - `docker`
 - `docker-compose`
 - `python3.10`
 - `python3.10-venv`

To install them on a debian based system run the following command.

```bash
sudo apt-get install git docker-compose python3.10-venv
```

# How Do I Use It?

After cloning this project to your system, make sure that all submodules
are initialized.

```bash
git submodule update --init
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

Once all dependencies are installed to virtual environment,
kytos can be run using the following command.

```bash
./run-kytos.sh
```

# Additional Notes

When running kytos, you may run into issues relating to mongodb.
MongoDB requires that your system has AVX instructions enabled.
If you are encountering such issues,
please check that AVX is enabled using the following command:

```
cat /proc/cpuinfo | grep avx
```

If AVX is enabled, you should see a few lines show with AVX highlighted.
If not, you will need to enable AVX.
