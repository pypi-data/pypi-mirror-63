"""
To pack:
  $ pip3 install wheel
  $ python3 setup.py sdist bdist_wheel

To upload to PyPI:
  $ python3 -m twine upload dist/*
"""

import setuptools

import stm32pio.app


with open('README.md', 'r') as readme:
    long_description = readme.read()


setuptools.setup(
    name='stm32pio',
    version=stm32pio.app.__version__,
    author='ussserrr',
    author_email='andrei4.2008@gmail.com',
    description="Small cross-platform Python app that can create and update PlatformIO projects from STM32CubeMX .ioc "
                "files. It uses STM32CubeMX to generate a HAL-framework-based code and alongside creates PlatformIO "
                "project with compatible parameters to stick them both together",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/ussserrr/stm32pio",
    packages=setuptools.find_packages(
        exclude=[
            'tests'
        ]
    ),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Topic :: Software Development :: Embedded Systems"
    ],
    keywords=[
        'platformio',
        'stm32',
        'stm32cubemx',
        'cubemx'
    ],
    python_requires='>=3.6',
    setup_requires=[
        'wheel'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'stm32pio = stm32pio.app:main'
        ]
    }
)
