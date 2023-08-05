import setuptools

setuptools.setup(
    name="catmouse",
    version="0.0.4",
    author="William Wyatt",
    author_email="tsangares@gmail.com",
    description="Mouse Logger for Science!",
    long_description="We catch the mouse for science.",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/Tsangares/cat_mouse",
    include_package_data=True,
    scripts=[
        'bin/cat.py',
        'bin/mouse.py',
    ],
    install_requires=[
        "Click==7.0",
        "Flask==1.1.1",
        "Flask-PyMongo==2.3.0",
        "itsdangerous==1.1.0",
        "Jinja2==2.11.1",
        "MarkupSafe==1.1.1",
        "pymongo==3.10.1",
        "Werkzeug==1.0.0",
        "certifi==2019.11.28",
        "chardet==3.0.4",
        "idna==2.9",
        "pynput==1.6.8",
        "python-xlib==0.26",
        "requests==2.23.0",
        "six==1.14.0",
        "urllib3==1.25.8",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
