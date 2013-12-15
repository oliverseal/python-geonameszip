from setuptools import setup
from setuptools.command.install import install

class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        install.run(self)

        # okay, we're installed
        from subprocess import call
        call([sys.executable, 'update.py'],
             cwd=os.path.join(dir, 'packagename'))

setup(
    name='geonameszip',
    version='0.1.0',
    description='Quick and dirty script/api for syncing postal codes / zip codes with a local sqlite3 database.',
    long_description=(open('README.md').read() + '\n\n' +
                      open('LICENSE.md').read()),
    url='https://github.com/oliverseal/python-geonameszip',
    license='MIT',
    author='Oliver Wilkerson',
    author_email='oliver.wilkerson@gmail.com',
    include_package_data=True,
    scripts=['update.py','terminal.py','README.md','LICENSE.md'],
    packages=['geonameszip'],
    package_dir={'geonameszip': './geonameszip'},
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