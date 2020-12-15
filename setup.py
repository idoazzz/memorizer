import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="memorizer-backend",
    version="0.0.1",
    author="Ido Azulay",
    author_email="idoazzz@gmail.com",
    description="Memorizer app package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idoazzz/memorizer",
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
)
