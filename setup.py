from setuptools import setup, find_packages

setup(
    name='webike-trip_detection',
    version='0.5.0',
    url='https://github.com/iss4e/webike-trip-detection',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    author='Information Systems and Science for Energy',
    author_email='webike-dev@lists.uwaterloo.ca',
    description='WeBike trip detection',
    packages=find_packages(),
    install_requires=[
        'iss4e_toolchain>=0.1.0',
        'kapacitor-udf'
    ]
)
