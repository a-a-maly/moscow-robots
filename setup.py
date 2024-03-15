import setuptools

setuptools.setup(
	name = "moscow_robots",
	version = "0.0.2",
	url = "https://github.com/mvrayko/moscow-robots",
	author = "Milya Rayko",
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
