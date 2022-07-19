from unittest import mock

import ganzo.sources as s


@mock.patch("google.cloud.storage.Client")
def test_me(_: mock.Mock):
    source = s.GCSSource("bucket_name")
    assert isinstance(source, s.GCSSource)
