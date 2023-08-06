from setuptools import setup, Extension, find_packages
import os

setup(
    name="travis_test",
    description="-",
    author="K0lb3",
    version="0.9.0",
    url="https://github.com/K0lb3/_travis_tests",
    ext_modules=[
        Extension(
            "travis_test",
            [
                os.path.join(root, f)
                for root, dirs, files in os.walk("src")
                for f in files
            ],
            language="c++",
            extra_compile_args=["-std=c++11"]
        )]
)
