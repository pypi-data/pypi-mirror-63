from setuptools import setup, find_namespace_packages

requirements = [
    "numpy",
    "opencv-python",
    "configparser",
    "napari",
]

setup(
    name="imgreg2D",
    version="0.0.0.1",
    author_email="federicoclaudi@protonmail.com",
    description="easy 2D image registration in python",
    packages=find_namespace_packages(exclude=()),
    include_package_data=True,
    install_requires=requirements,
    url="https://github.com/BrancoLab/imgreg2D",
    author="Federico Claudi, Philip Shamash",
    zip_safe=False,
)
