import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="pmdatapipelines-light",
	version="0.0.1",
	author="Jørgen Frøland",
	author_email="jorgen.froland@polarismedia.no",
	description="Lightweight version of data pipeline library for Polaris Media",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="",
	packages=setuptools.find_packages(),
	install_requires=[
		'boto3'
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)