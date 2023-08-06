import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='rapid-desktop-switcher',
    version='0.1.0',
    author="Bruce Blore",
    author_email="bruceblore@protonmail.com",
    description="Change your virtual desktop with the press of a key. Helpful as a panic button.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://example.com",
    packages=setuptools.find_packages(),
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
    ],
)
