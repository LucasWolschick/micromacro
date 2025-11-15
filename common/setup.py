from setuptools import setup, find_packages

setup(
    name="common",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["fastapi", "asyncpg", "aio-pika"],
    extras_require={"dev": ["asyncpg-stubs"]},
)
