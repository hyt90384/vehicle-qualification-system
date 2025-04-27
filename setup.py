from setuptools import setup, find_packages

setup(
    name="vehicle-qualification-system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'sqlalchemy',
        'easyocr',
        'alembic'
    ],
) 