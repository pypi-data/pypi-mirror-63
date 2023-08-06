import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xraydawgz",
    version="0.1",
    license='MIT',
    author="Rick, Alex, Robert, Kevin",
    author_email = 'rbiegaj@uw.edu',
    description="XRayDawgz XRD image pattern classifier",
    url="https://github.com/X-ray-Dawgz/XRayDawgz",
    download_url = 'https://github.com/X-ray-Dawgz/XRayDawgz/archive/v_01.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=[
        'tensorflow',
        'keras.preprocessing',
        'numpy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
