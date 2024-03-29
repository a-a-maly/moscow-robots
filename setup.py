import setuptools

setuptools.setup(
	name = "moscow_robots",
	version = "0.0.3",
	url = "https://github.com/a-a-maly/moscow-robots.git",
	author = "Alexander A. Maly",
	description = "Moscow Robots library support",
	long_description = open('README.md').read(),
	packages = setuptools.find_packages(),
	install_requires = ['pygame', 'Pillow'],
	classifiers = [
		'Programming Language :: Python :: 3',
	],
	include_package_data = True,
	package_data = {'' : ['textures/*.png']}
)
