from setuptools import find_packages, setup

setup(
    name='Budget API',
    version='0.5.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
