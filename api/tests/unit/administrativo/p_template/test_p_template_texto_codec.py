import pytest

from actions.data.rtf_blob_codec import RTFBlobCodec


@pytest.mark.unit
def test_rtf_blob_codec_roundtrip():
    rtf = r"{\rtf1\ansi\deff0 {\fonttbl {\f0 Arial;}}\f0\fs22 Texto de teste}"

    blob = RTFBlobCodec.rtf_text_to_blob(rtf)
    decoded = RTFBlobCodec.blob_to_rtf_text(blob)

    assert isinstance(blob, bytes)
    assert decoded.startswith(r"{\rtf1")
    assert "Texto de teste" in decoded


@pytest.mark.unit
def test_rtf_blob_codec_handles_python_bytes_repr_string():
    rtf = r"{\rtf1\ansi\deff0 {\fonttbl {\f0 Arial;}}\f0\fs22 Texto blob repr}"
    blob = RTFBlobCodec.rtf_text_to_blob(rtf)
    blob_repr = repr(blob)

    decoded = RTFBlobCodec.blob_to_rtf_text(blob_repr)

    assert decoded.startswith(r"{\rtf1")
    assert "Texto blob repr" in decoded

