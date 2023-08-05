# SPDX-License-Identifier: GPL-3.0-or-later

# Copyright 2019, 2020 igo95862

# This file is part of bubblejail.
# bubblejail is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# bubblejail is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with bubblejail.  If not, see <https://www.gnu.org/licenses/>.


from setuptools import setup, find_packages

setup(
    name="bubblejail",
    description=("Use AUR to install bubblejail. "
                 "PyPI package is only to hold place."),
    url='https://github.com/igo95862/bubblejail',
    version="0.2",
    packages=find_packages(
        exclude=['test']
    ),
    entry_points={
        'console_scripts': [
            'bubblejail = bubblejail.bubblejail_cli:bubblejail_main',
            ('bubblejail-helper = '
             'bubblejail.bubblejail_helper:bubblejail_helper_main'),
        ],
    },
    package_data={
        'bubblejail': ['profiles/*toml'],
    },
)
