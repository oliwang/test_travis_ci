import pytest

# import sys
# sys.path.append('../src/mypkg')

from mypkg.content_extract import *
# from Content_Extract import *


def test_url():
    url = "https://www.cnn.com/2018/10/29/europe/angela-merkel-germany-election-intl/index.html"
    assert(generate_content(url)[
           "title"] == "Angela Merkel, German Chancellor, to step down in 2021")
