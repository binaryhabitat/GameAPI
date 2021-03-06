import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='GameAPI',
    version='0.1.1',
    description="GameAPI is a library for interacting with popular Game APIs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='BinaryHabitat',
    packages=setuptools.find_packages(exclude=["tests.*", "tests"]),
    python_requires='>=3.8',
    install_requires=[
        'httpx==0.17'
    ]
)
