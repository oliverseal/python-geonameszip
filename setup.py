from setuptools import setup
from setuptools.command.install import install

class InstallAndUpdateCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        install.run(self)

        try:
          # okay, we're installed
          from geonameszip import update
          update.download()
          update.import_downloaded_file()
        except OSError:
          print('Error getting the initial database setup. Run update_geonameszip.py as an administrator.')

setup(
    name='geonameszip',
    version='0.2.3',
    description='Quick and dirty script/api for syncing postal codes / zip codes with a local sqlite3 database.',
    long_description=(open('README.md').read() + '\n\n' +
                      open('LICENSE.md').read()),
    url='https://github.com/oliverseal/python-geonameszip',
    license='MIT',
    author='Oliver Wilkerson',
    author_email='oliver.wilkerson@gmail.com',
    include_package_data=True,
    scripts=['update_geonameszip.py'],
    packages=['geonameszip'],
    package_dir={'geonameszip': './geonameszip'},
    cmdclass={'install': InstallAndUpdateCommand },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
