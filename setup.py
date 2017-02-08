"""
Author: Berty Pribilovics

A Bottle based REST API.

"""


from setuptools import setup

setup(
    name="Micro URL",
    version="0.1",
    description="URL shortening service the device type detection and routing",
    author="Berty Pribilovics",
    author_email="bpribilovics@gmail.com",
    packages=["micro_url"],
    install_requires=[
        "bottle",
        "short_url",
        "user_agents"
    ]
)
