from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup_requirements = ['pytest-runner']

test_requirements = ['pytest']


setup(
    name='pyavro',
    author='Mitchell Lisle',
    author_email='m.lisle90@gmail.com',
    description="A Python Avro Schema Builder",
    install_requires=requirements,
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mitchelllisle/pyavro',
    version='0.1.0',
    zip_safe=False,
)
