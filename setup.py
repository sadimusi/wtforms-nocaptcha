from setuptools import setup

setup(
    name='wtforms-nocaptcha',
    version=__import__('wtfnocaptcha').__version__,
    url='https://github.com/evrom/wtforms-nocaptcha/',
    license='BSD',
    author='Evan Roman',
    author_email='evanroman1@gmail.com',
    description='Custom WTForms field that handles No Captcha reCaptcha '
    'display and validation',
    long_description=open('README.rst').read(),
    platforms='any',
    packages=['wtfnocaptcha'],
    install_requires=['WTForms>=0.6.1'],
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
