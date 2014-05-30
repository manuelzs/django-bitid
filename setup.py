from setuptools import setup

setup(
    name='django-bitid',
    version='0.1',
    description='App for django bitId authentication',
    author='Manuel Zapata',
    author_email='manuelzs@gmail.com',
    url='http://github.com/manuelzs/django-bitid/',
    long_description=open('README.rst', 'r').read(),
    packages=[
        'djbitid',
    ],
    package_data={
        'djbitid': ['templates/djbitid/*'],
    },
    zip_safe=False,
    requires=[
        'south(>=0.8.4)',
        'pytz(>=2014.3)',
    ],
    install_requires=[
        'south >= 0.8.4',
        'pytz >= 2014.3',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
