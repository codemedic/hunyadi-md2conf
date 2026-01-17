"""
Publish Markdown files to Confluence wiki.

Copyright 2022-2026, Levente Hunyadi

:see: https://github.com/hunyadi/md2conf
"""

from md2conf.markdown import filter_markdown
from tests.utility import TypedTestCase


class TestFilter(TypedTestCase):
    def test_block_skip(self) -> None:
        content = """# Title
<!-- confluence-skip-start -->
This is a block of text
that should be skipped.
<!-- confluence-skip-end -->
Visible text."""
        expected = """# Title

Visible text."""
        self.assertEqual(filter_markdown(content), expected)

    def test_inline_skip(self) -> None:
        content = "This is <!-- confluence-skip-start -->hidden<!-- confluence-skip-end --> visible."
        expected = "This is  visible."
        self.assertEqual(filter_markdown(content), expected)

    def test_multiple_skips(self) -> None:
        content = """Start.
<!-- confluence-skip-start -->
Skip 1
<!-- confluence-skip-end -->
Middle.
<!-- confluence-skip-start -->
Skip 2
<!-- confluence-skip-end -->
End."""
        expected = """Start.

Middle.

End."""
        self.assertEqual(filter_markdown(content), expected)

    def test_whitespace_variations(self) -> None:
        # no interior spaces
        content = "A<!--confluence-skip-start-->B<!--confluence-skip-end-->C"
        expected = "AC"
        self.assertEqual(filter_markdown(content), expected)

        # excessive interior spaces
        content = "A<!--   confluence-skip-start   -->B<!--   confluence-skip-end   -->C"
        expected = "AC"
        self.assertEqual(filter_markdown(content), expected)

        # newline in comment
        content = "A<!--\nconfluence-skip-start\n-->B<!--\nconfluence-skip-end\n-->C"
        expected = "AC"
        self.assertEqual(filter_markdown(content), expected)

    def test_unbalanced_markers(self) -> None:
        # only start
        content = "<!-- confluence-skip-start --> Hidden"
        with self.assertRaises(ValueError):
            filter_markdown(content)

        # only end
        content = "Hidden <!-- confluence-skip-end -->"
        with self.assertRaises(ValueError):
            filter_markdown(content)

    def test_nested(self) -> None:
        # nested markers: start ... start ... end ... end
        content = "1<!-- confluence-skip-start -->2<!-- confluence-skip-start -->3<!-- confluence-skip-end -->4<!-- confluence-skip-end -->5"
        with self.assertRaises(ValueError):
            filter_markdown(content)

    def test_out_of_order(self) -> None:
        # end before start
        content = "A <!-- confluence-skip-end --> B <!-- confluence-skip-start --> C"
        with self.assertRaises(ValueError):
            filter_markdown(content)

