from setuptools import setup
import setuptools
from setuptools.command.test import test as TestCommand
with open("README.md", "r") as f:
        long_description = f.read()

print(setuptools.find_packages(exclude=["tests"]))

class ToxTest(TestCommand):
    user_options = []
    def initialize_options(self):
        TestCommand.initialize_options(self)
        def run_tests(self):
            import tox
            tox.cmdline()

setup( name='lazymappingstorage',
       version='0.0.2',
       description='A dict like storage backed by a yaml file or similar method',
       url='',
       author='Andreas Stephanides',
       author_email='st-andreas@gmx.at',
       long_description=long_description,
       long_description_content_type="text/markdown",
       py_modules=["lazymappingstorage"],
       package_dir={'': 'src'},
       install_requires=[
           'PyYAML'
       ],
#       test_suite='nose.collector',
       extras_require = {
               "dev": ["pytest>=3.7",]
       },
#       tests_require=['pytest'],
       zip_safe=False,
       cmdclass={'test': ToxTest}
)
