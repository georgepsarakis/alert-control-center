import os
from setuptools import setup, find_packages


requirements = dict.fromkeys(('dev', 'test', 'base'))

for section in requirements:
    file_path = os.path.join('requirements', '{}.txt'.format(section))
    with open(file_path, 'r') as f:
        requirements[section] = list(f.readlines())

setup(
    name='alert-manager',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=requirements['base'],
    extras_require=requirements,
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
    ],
)

