from setuptools import setup

setup(
    name='pali_bot',
    version='0.0.1',
    author='Alexandr Cherkaev',
    author_email=None,  # TODO
    python_requires='>=3.9',
    url='https://github.com/Alexandr4812/pali_bot',
    license='Apache',
    description='Telegram bot to read suttas',
    install_requires=(
        'python-telegram-bot~=13.13',
        'PyYAML~=6.0',
    ),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pali_bot= pali_bot.__main__:main',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    py_modules=['pali_bot'])
