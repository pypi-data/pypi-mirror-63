# Copyright 2015, Ansible, Inc.
# Luke Sneeringer <lsneeringer@ansible.com>
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


import os
import sys
from test.compat import unittest

# Ensure that the tests directory is part of our Python path.
APP_ROOT = os.path.realpath(os.path.dirname(__file__) + '/../')
sys.path.append(APP_ROOT)


# Find tests.
def load_tests(loader, standard_tests, throwaway):
    return loader.discover('tests')


# Run the tests.
if __name__ == '__main__':
    unittest.main()
