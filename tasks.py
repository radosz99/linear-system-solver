import invoke
import pathlib


@invoke.task
def clean(c):
    """ Remove any built objects """
    for pattern in ["*.o", "*.so"]:
        c.run("rm -rf {}".format(pattern))


def print_banner(msg):
    print("==================================================")
    print("= {} ".format(msg))


def compile_python_module(cpp_name, extension_name):
    invoke.run(
        "g++ -O3 -Wall -Werror -shared -std=c++11 -fPIC "
        "`python3 -m pybind11 --includes` "
        "-I /usr/include/python3.7 -I .  "
        "{0} "
        "-o {1}`python3.8-config --extension-suffix` "
        "-L.  -Wl,-rpath,.".format(cpp_name, extension_name)
    )

@invoke.task()
def build_solver(c):
    """ Build the pybind11 wrapper library """
    print_banner("Building PyBind11 Module for solving systems of linear equations")
    compile_python_module("wrapper.cpp", "equations_solver")
    print("* Complete")

@invoke.task(
    clean,
    build_solver,
)

def all(c):
    """ Build and run all tests """
    pass
