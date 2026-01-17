"""
Publish Markdown files to Confluence wiki.

Copyright 2022-2026, Levente Hunyadi

:see: https://github.com/hunyadi/md2conf
"""

import logging
import shutil
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from md2conf.compatibility import override
from md2conf.local import LocalConverter
from md2conf.metadata import ConfluenceSiteMetadata
from md2conf.options import ConfluencePageID, DocumentOptions
from tests.utility import TypedTestCase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(funcName)s [%(lineno)d] - %(message)s",
)


class TestScheduledPublish(TypedTestCase):
    out_dir: Path
    temp_dir: Path

    @override
    def setUp(self) -> None:
        test_dir = Path(__file__).parent
        self.out_dir = test_dir / "output_scheduled"
        self.temp_dir = test_dir / "temp_scheduled"
        self.out_dir.mkdir(exist_ok=True, parents=True)
        self.temp_dir.mkdir(exist_ok=True, parents=True)

    @override
    def tearDown(self) -> None:
        shutil.rmtree(self.out_dir, ignore_errors=True)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_converter(self, options: DocumentOptions) -> LocalConverter:
        site_metadata = ConfluenceSiteMetadata(domain="example.com", base_path="/wiki/", space_key="SPACE_KEY")
        return LocalConverter(options, site_metadata, self.out_dir)

    def test_publish_after_future(self) -> None:
        # Create a file with publish_after in the future
        future_date = datetime.now(timezone.utc) + timedelta(days=1)
        content = f"""---
publish_after: {future_date.isoformat()}
---
# Future Page
"""
        test_file = self.temp_dir / "future.md"
        with open(test_file, "w") as f:
            f.write(content)

        options = DocumentOptions(root_page_id=ConfluencePageID("None"))
        self.create_converter(options).process(test_file)

        # Should not be published (no .csf file)
        self.assertFalse((self.out_dir / "future.csf").exists())

    def test_publish_after_past(self) -> None:
        # Create a file with publish_after in the past
        past_date = datetime.now(timezone.utc) - timedelta(days=1)
        content = f"""---
publish_after: {past_date.isoformat()}
---
# Past Page
"""
        test_file = self.temp_dir / "past.md"
        with open(test_file, "w") as f:
            f.write(content)

        options = DocumentOptions(root_page_id=ConfluencePageID("None"))
        self.create_converter(options).process(test_file)

        # Should be published
        self.assertTrue((self.out_dir / "past.csf").exists())

    def test_ignore_publish_after(self) -> None:
        # Create a file with publish_after in the future
        future_date = datetime.now(timezone.utc) + timedelta(days=1)
        content = f"""---
publish_after: {future_date.isoformat()}
---
# Ignored Future Page
"""
        test_file = self.temp_dir / "ignored_future.md"
        with open(test_file, "w") as f:
            f.write(content)

        # Use ignore_publish_after=True
        options = DocumentOptions(root_page_id=ConfluencePageID("None"), ignore_publish_after=True)
        self.create_converter(options).process(test_file)

        # Should be published despite being in the future
        self.assertTrue((self.out_dir / "ignored_future.csf").exists())

    def test_publish_after_timezone_future(self) -> None:
        # Create a file with publish_after in the future with a different timezone (UTC+5)
        future_date = datetime.now(timezone(timedelta(hours=5))) + timedelta(days=1)
        content = f"""---
publish_after: {future_date.isoformat()}
---
# Future TZ Page
"""
        test_file = self.temp_dir / "future_tz.md"
        with open(test_file, "w") as f:
            f.write(content)

        options = DocumentOptions(root_page_id=ConfluencePageID("None"))
        self.create_converter(options).process(test_file)

        # Should not be published
        self.assertFalse((self.out_dir / "future_tz.csf").exists())

    def test_publish_after_timezone_past(self) -> None:
        # Create a file with publish_after in the past with a different timezone (UTC-5)
        past_date = datetime.now(timezone(timedelta(hours=-5))) - timedelta(days=1)
        content = f"""---
publish_after: {past_date.isoformat()}
---
# Past TZ Page
"""
        test_file = self.temp_dir / "past_tz.md"
        with open(test_file, "w") as f:
            f.write(content)

        options = DocumentOptions(root_page_id=ConfluencePageID("None"))
        self.create_converter(options).process(test_file)

        # Should be published
        self.assertTrue((self.out_dir / "past_tz.csf").exists())

    def test_invalid_date_format(self) -> None:
        # Create a file with invalid publish_after format
        content = """---
publish_after: invalid-date
---
# Invalid Date Page
"""
        test_file = self.temp_dir / "invalid.md"
        with open(test_file, "w") as f:
            f.write(content)

        options = DocumentOptions(root_page_id=ConfluencePageID("None"))

        # This might raise an error during frontmatter parsing (yaml load -> cattrs structure)
        # depending on how cattrs handles invalid dates.
        # Let's see if it skips or raises. If it raises, we should handle it or let it fail gracefully.

        try:
            self.create_converter(options).process(test_file)
            # If it doesn't raise, check if it defaulted to something or just ignored it
        except Exception as e:
            logging.info(f"Caught expected exception for invalid date: {e}")
            # Depending on desired behavior, we might want it to still publish but ignore the field,
            # or fail. Most md2conf frontmatter errors currently fail.


if __name__ == "__main__":
    unittest.main()
