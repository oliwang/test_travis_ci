import pytest

import sys
sys.path.append('..')

from content_extract import *


def test_url():
    url = "https://www.cnn.com/2018/10/29/europe/angela-merkel-germany-election-intl/index.html"
    assert(generate_content(url)[
           "title"] == "Angela Merkel, German Chancellor, to step down in 2021")
