"""
Publish Markdown files to Confluence wiki.

Copyright 2022-2025, Levente Hunyadi

:see: https://github.com/hunyadi/md2conf
"""

import logging
import os
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from md2conf.plantuml import (
    PlantUMLConfigProperties,
    get_available_themes,
    has_plantuml,
    render_diagram,
    validate_theme,
)
from tests.utility import TypedTestCase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(funcName)s [%(lineno)d] - %(message)s",
)

PLANTUML_SOURCE = """
@startuml
abstract class Animal {
  +name: String
  +age: int
  +makeSound(): void
}

class Dog {
  +breed: String
  +bark(): void
  +makeSound(): void
}

class Cat {
  +color: String
  +meow(): void
  +makeSound(): void
}

Animal <|-- Dog
Animal <|-- Cat
@enduml
"""


@unittest.skipUnless(has_plantuml(), "plantuml is not available")
@unittest.skipUnless(os.getenv("TEST_PLANTUML"), "plantuml tests are disabled")
class TestPlantumlRendering(TypedTestCase):
    def test_render_simple_svg(self) -> None:
        svg = render_diagram(PLANTUML_SOURCE, output_format="svg")
        root = ET.fromstring(svg)
        self.assertTrue(root.tag.lower() == "svg" or root.tag.endswith("}svg"))

    def test_render_simple_png(self) -> None:
        png = render_diagram(PLANTUML_SOURCE)
        self.assertIn(b"PNG", png)


@unittest.skipUnless(has_plantuml(), "plantuml is not available")
@unittest.skipUnless(os.getenv("TEST_PLANTUML"), "plantuml tests are disabled")
class TestPlantumlThemes(TypedTestCase):
    def test_get_available_themes(self) -> None:
        """Test that we can retrieve list of available themes."""
        themes = get_available_themes()
        self.assertIsInstance(themes, list)
        self.assertGreater(len(themes), 0)
        # Check for some common themes
        self.assertIn("_none_", themes)
        self.assertIn("bluegray", themes)

    def test_validate_valid_theme(self) -> None:
        """Test that valid themes pass validation."""
        # Should not raise
        validate_theme("bluegray")
        validate_theme("_none_")

    def test_validate_invalid_theme(self) -> None:
        """Test that invalid themes raise RuntimeError."""
        with self.assertRaises(RuntimeError) as context:
            validate_theme("nonexistent_theme_xyz")
        self.assertIn("not found", str(context.exception))
        self.assertIn("Available themes:", str(context.exception))

    def test_render_with_theme(self) -> None:
        """Test rendering diagram with a theme."""
        config = PlantUMLConfigProperties(theme="bluegray")
        svg = render_diagram(PLANTUML_SOURCE, output_format="svg", config=config)
        root = ET.fromstring(svg)
        self.assertTrue(root.tag.lower() == "svg" or root.tag.endswith("}svg"))


@unittest.skipUnless(has_plantuml(), "plantuml is not available")
@unittest.skipUnless(os.getenv("TEST_PLANTUML"), "plantuml tests are disabled")
class TestPlantumlSkinparams(TypedTestCase):
    def test_render_with_skinparams(self) -> None:
        """Test rendering diagram with skinparam settings."""
        config = PlantUMLConfigProperties(
            skinparams={
                "backgroundColor": "white",
                "classBackgroundColor": "#FEFECE",
            }
        )
        svg = render_diagram(PLANTUML_SOURCE, output_format="svg", config=config)
        root = ET.fromstring(svg)
        self.assertTrue(root.tag.lower() == "svg" or root.tag.endswith("}svg"))

    def test_render_with_multiple_skinparams(self) -> None:
        """Test rendering with multiple skinparam settings."""
        config = PlantUMLConfigProperties(
            skinparams={
                "backgroundColor": "transparent",
                "shadowing": "false",
                "classBackgroundColor": "#EEEBDC",
                "classBorderColor": "#181818",
            }
        )
        png = render_diagram(PLANTUML_SOURCE, output_format="png", config=config)
        self.assertIn(b"PNG", png)


@unittest.skipUnless(has_plantuml(), "plantuml is not available")
@unittest.skipUnless(os.getenv("TEST_PLANTUML"), "plantuml tests are disabled")
class TestPlantumlIncludes(TypedTestCase):
    def test_render_with_include(self) -> None:
        """Test rendering diagram with include file."""
        # Create a temporary include file with custom styling
        with tempfile.NamedTemporaryFile(mode="w", suffix=".puml", delete=False) as f:
            f.write("!define CUSTOM_COLOR #FF0000\n")
            f.write("skinparam classBackgroundColor CUSTOM_COLOR\n")
            include_path = f.name

        try:
            config = PlantUMLConfigProperties(includes=[include_path])
            svg = render_diagram(PLANTUML_SOURCE, output_format="svg", config=config)
            root = ET.fromstring(svg)
            self.assertTrue(root.tag.lower() == "svg" or root.tag.endswith("}svg"))
        finally:
            Path(include_path).unlink()

    def test_render_with_multiple_includes(self) -> None:
        """Test rendering with multiple include files."""
        # Create temporary include files
        include_files = []
        for i in range(2):
            with tempfile.NamedTemporaryFile(mode="w", suffix=".puml", delete=False) as f:
                f.write(f"!define CUSTOM_{i} value_{i}\n")
                include_files.append(f.name)

        try:
            config = PlantUMLConfigProperties(includes=include_files)
            png = render_diagram(PLANTUML_SOURCE, output_format="png", config=config)
            self.assertIn(b"PNG", png)
        finally:
            for path in include_files:
                Path(path).unlink()


@unittest.skipUnless(has_plantuml(), "plantuml is not available")
@unittest.skipUnless(os.getenv("TEST_PLANTUML"), "plantuml tests are disabled")
class TestPlantumlCombinedConfig(TypedTestCase):
    def test_render_with_all_options(self) -> None:
        """Test rendering with theme, skinparams, includes, and scale."""
        # Create a temporary include file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".puml", delete=False) as f:
            f.write("skinparam classFontSize 14\n")
            include_path = f.name

        try:
            config = PlantUMLConfigProperties(
                theme="bluegray",
                skinparams={"backgroundColor": "white", "shadowing": "false"},
                includes=[include_path],
                scale=1.5,
            )
            svg = render_diagram(PLANTUML_SOURCE, output_format="svg", config=config)
            root = ET.fromstring(svg)
            self.assertTrue(root.tag.lower() == "svg" or root.tag.endswith("}svg"))
        finally:
            Path(include_path).unlink()


if __name__ == "__main__":
    unittest.main()
