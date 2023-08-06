# Copyright 2020 Jacques Supcik
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path

from setuptools import setup, find_packages

with open(Path(__file__).parent / 'README.rst') as f:
    long_description = f.read()

setup(
    name='pymdown-include',
    packages=find_packages(exclude=["tests"]),
    version='0.0.1',
    description='Include...',
    long_description=long_description,
    author='Jacques Supcik',
    author_email='jacques@supcik.net',
    url='https://github.com/supcik/pymdown-include/',
    keywords=['Markdown', 'include', 'extension'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'markdown.extensions': ['include = pymdown_include:PymdownInclude'],
    },
    install_requires=['markdown']
)
