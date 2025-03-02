import unittest
import textwrap

from generate import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self) -> None:
        md = "#  Title "
        self.assertEqual(extract_title(md), "Title")
        md = textwrap.dedent("""\
            Lots of lines
            ## Not Yet
            # Title found
            ### Should reach here      
        """)
        self.assertEqual(extract_title(md), "Title found")
