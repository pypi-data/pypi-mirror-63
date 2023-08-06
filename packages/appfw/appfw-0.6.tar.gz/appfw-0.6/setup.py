import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='appfw',
    version='0.6',
    author="Ergin Soysal",
    author_email="esoysal@gmail.com",
    description="Application framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soysal/appfw",
    packages=setuptools.find_packages(),
    package_data={'appfw': ['tpl/*.tpl']},
    entry_points={
        'console_scripts': ['app-init=appfw.app_init:run'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
