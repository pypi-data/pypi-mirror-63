from setuptools import setup, find_packages

setup(
    name="nameko-sematext-logger",
    version="0.0.1rc1",
    packages=find_packages(exclude=["test", "test.*"]),
    description="Nameko extension for sematext logging",
    long_description=open("README.md").read(),
    author="Raman Damodar Shahdadpuri",
    author_email="raman@gritfirst.com",
    long_description_content_type="text/markdown",
    url="https://github.com/raman-grit/nameko-sematext-logger",
    install_requires=["nameko>=2.7.0"],
    dependency_links=[],
    zip_safe=True,
    license="GritFirst"
)