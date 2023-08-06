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

import inspect
import unittest
from pathlib import Path

import markdown

from pymdown_include import PymdownInclude


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.md = markdown.Markdown(
            extensions=[PymdownInclude(SEARCH_PATH=[Path(__file__).parent])]
        )

    def test_simple(self):

        MD = """
            # h1
            Hello
            ## h2
            World
        """

        HTML = """
            <h1>h1</h1>
            <p>Hello</p>
            <h2>h2</h2>
            <p>World</p>
        """

        self.assertEqual(self.md.convert(
            inspect.cleandoc(MD)), inspect.cleandoc(HTML))

    def test_one_line(self):

        MD = """
            A {!one_line.txt!} B
        """

        HTML = """
            <p>A line 1 B</p>
        """

        self.assertEqual(self.md.convert(
            inspect.cleandoc(MD)), inspect.cleandoc(HTML))

if __name__ == '__main__':
    unittest.main()
