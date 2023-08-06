import setuptools

with open('README.md') as f:
	long_description = f.read()

setuptools.setup(
	name='minimal-lagrangians',
	version='1.0.0',
	author='Simon May',
	author_email='simon.may@mpa-garching.mpg.de',
	description='A Python program to generate the Lagrangians for dark matter models',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://gitlab.com/Socob/minimal-lagrangians',
	keywords='particle physics, beyond the standard model, dark matter',
	packages=setuptools.find_packages(),
	package_data={'': ['data/*']},
	license='GNU GPLv3',
	platforms='OS Independent',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: OS Independent',
		'Topic :: Scientific/Engineering :: Physics',
		'Intended Audience :: Science/Research',
		'Natural Language :: English',
	],
	python_requires='>=3.4',
	scripts=['minimal-lagrangians', 'minimal-lagrangians.py']
)
