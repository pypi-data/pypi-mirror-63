import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testwizard.web",
    version="3.1.19",
    author="Eurofins Digital Testing - Belgium",
    author_email="support-be@eurofins.com",
    description="Testwizard for Web testobjects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['testwizard.web'],
    install_requires=[
        'testwizard.core==3.1.19',
        'testwizard.testobjects-core==3.1.19',
        'testwizard.commands-audio==3.1.19',
        'testwizard.commands-video==3.1.19',
        'testwizard.commands-web==3.1.19'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
    ],
)




































