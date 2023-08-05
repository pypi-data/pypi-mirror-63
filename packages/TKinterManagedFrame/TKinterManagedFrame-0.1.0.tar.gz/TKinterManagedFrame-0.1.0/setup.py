import setuptools
from distutils.core import setup
with open('README.md') as file_:
	long_description = file_.read()
setup(
	name='TKinterManagedFrame',
	packages=['TKinterManagedFrame'],
	version='0.1.0',
	license='GNU GPL',
	description='Adds a Tkinter Frame class that offers simple update functionality',
	long_description=long_description,
	long_description_content_type='text/markdown',
	author='Christopher "Arkevorkhat" Trent',
	url='https://github.com/ChristopherJTrent/TKinterManagedFrame',
	install_requires=['tkinter','wheel'],
	python_requires='>=3.3',
	classifiers=[
			  'Development Status :: 3 - Alpha', 
			  'Intended Audience :: Developers',
			  'Topic :: Software Development :: Libraries :: Tcl Extensions',
			  'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
			  'Natural Language :: English',
			  'Programming Language :: Python :: 3.3',
			  'Programming Language :: Python :: 3.4',
			  'Programming Language :: Python :: 3.5',
			  'Programming Language :: Python :: 3.6',
			  'Programming Language :: Python :: 3.7',
			  'Programming Language :: Python :: 3.8',
			  'Programming Language :: Python :: 3.9'
			  ]
)
