__version__ = '0.1.0'
__author__ = 'Sondre Lillebø Gundersen'

from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.rst') as changelog_file:
    changelog = changelog_file.read()

setup(
    name='django-swagger-tester',
    version=__version__,
    description='Test utility for asserting that your API outputs actually match your OpenAPI/Swagger specification.',
    py_modules=['django_swagger_tester'],
    include_package_data=True,
    long_description=readme + '\n\n' + changelog,
    license='BSD',
    author=__author__,
    author_email='sondrelg@live.no',
    url='https://github.com/sondrelg/django-swagger-tester',
    download_url='https://pypi.python.org/pypi/django-swagger-tester',
    packages=find_packages(exclude=['']),
    install_requires=['djangorestframework', 'PyYAML', 'django'],
    keywords=['openapi', 'swagger', 'api', 'test', 'testing', 'drf_yasg', 'django'],
    platforms='OS Independent',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Pytest',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Documentation',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Unit',
    ],
)
