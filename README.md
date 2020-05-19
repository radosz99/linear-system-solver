**<p align="center"> Wrocław University of Science and Technology </p>**
**<p align="center"> Computer Science, Faculty of Electronics, 6 semester </p>**
<p align="center"> Radosław Lis, 241385 </p>

# Table of Contents
- [General info](#desc)
- [Run](#run)
- [Build executable](#build)
<a name="desc"></a>
# General info
Python & C++ application for solving linear systems.

<a name="run"></a>
# Run

```
$ pip3 install -r requirements.txt 
$ invoke build-solver
$ python3 solve.py
```
<a name="build"></a>
# Build and run executable

```
$ pyinstaller --clean -F solve.py && cd dist
$ ./solve
```
