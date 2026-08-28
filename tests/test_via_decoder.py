"""Tests for the Via header decoder used by content/via.html.

The decoder lives in content/js/via-decoder.js and is shared between the
website (browser) and these tests (node). Each test shells out to node and
decodes a via string, then asserts on the structured result.

The parser is tag-driven, mirroring traffic_via.cc from apache/trafficserver:
lowercase letters are field tags, uppercase letters and spaces are values,
':' or ';' separates the standard section from the detail section.

Run with: pytest tests/
"""

import json
import pathlib
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
DECODER = ROOT / "content" / "js" / "via-decoder.js"

NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="node is required to run the decoder")

DRIVER = "const d = require(process.argv[1]); process.stdout.write(JSON.stringify(d.decodeVia(process.argv[2])));"


def decode(via):
    result = subprocess.run(
        [NODE, "-e", DRIVER, str(DECODER), via],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def field(result, title_fragment):
    matches = [f for f in result["fields"] if title_fragment.lower() in f["title"].lower()]
    assert matches, f"no field with title containing {title_fragment!r} in {result['fields']}"
    assert len(matches) == 1, f"ambiguous title fragment {title_fragment!r}"
    return matches[0]


def test_via_missing_client_pair_and_trailing_space():
    """The reported bug: a via with no leading u<x> client pair and the
    trailing space (origin connection value) lost in copy/paste."""
    result = decode("cMsSfWpSeN:t cCMpSs")
    assert result["ok"] is True

    assert field(result, "cache lookup for URL")["code"] == "M"
    assert field(result, "Response information")["code"] == "S"
    assert field(result, "write-to-cache")["code"] == "W"
    assert field(result, "Proxy operation")["code"] == "S"
    assert field(result, "Error codes")["code"] == "N"
    assert "no error" in field(result, "Error codes")["description"]

    assert field(result, "Tunnel")["code"] == " "
    assert field(result, "Cache Type")["code"] == "C"
    assert field(result, "Cache Lookup Result")["code"] == "M"
    assert field(result, "Parent proxy")["code"] == "S"
    # The trailing space was stripped; the missing value must decode as ' '.
    assert field(result, "server connection status")["code"] == " "

    # No client-info tag in the input, so no client field in the output.
    assert not any("received from client" in f["title"] for f in result["fields"])


def test_canonical_full_via():
    result = decode("uScMsSfWpSeN:t cCMp sS")
    assert result["ok"] is True
    assert field(result, "received from client")["code"] == "S"
    assert field(result, "cache lookup for URL")["code"] == "M"
    assert field(result, "Parent proxy")["code"] == " "
    assert field(result, "server connection status")["code"] == "S"


def test_full_header_line_with_brackets():
    header = "HTTP/1.1 proxy.example.com (ApacheTrafficServer/10.0.0 [uScMsSfWpSeN:t cCMpSs ])"
    result = decode(header)
    assert result["ok"] is True
    assert field(result, "received from client")["code"] == "S"
    assert field(result, "Parent proxy")["code"] == "S"
    assert field(result, "server connection status")["code"] == " "


def test_legacy_24_char_via_with_icp_tag():
    """Pre-8.0 vias are 24 chars and include an 'i' (ICP) tag; it must be
    tolerated without derailing the rest of the decode."""
    result = decode("[uScMsSf pSeN:t cCMi p sS]")
    assert result["ok"] is True
    assert field(result, "write-to-cache")["code"] == " "
    assert field(result, "Cache Lookup Result")["code"] == "M"
    assert field(result, "Parent proxy")["code"] == " "
    assert field(result, "server connection status")["code"] == "S"


def test_short_response_via():
    result = decode("cMsSfW")
    assert result["ok"] is True
    assert field(result, "cache lookup for URL")["code"] == "M"
    assert field(result, "Response information")["code"] == "S"
    assert field(result, "write-to-cache")["code"] == "W"


def test_short_response_via_stripped_trailing_space():
    result = decode("cMsSf")
    assert result["ok"] is True
    assert field(result, "write-to-cache")["code"] == " "


def test_semicolon_separator():
    """Some ATS versions emit ';' instead of ':' before the detail section."""
    result = decode("[u c s f p eS;tNc  p s ]")
    assert result["ok"] is True
    assert "server related error" in field(result, "Error codes")["description"]
    assert "no forward" in field(result, "Tunnel")["description"]
    assert field(result, "Cache Type")["code"] == " "


def test_read_while_write_hit():
    """'W' is a valid cache-lookup result (read-while-write hit)."""
    result = decode("uScWsSfWpSeN:t cCHp sS")
    assert result["ok"] is True
    assert "Read While Write" in field(result, "cache lookup for URL")["description"]


def test_unknown_value_is_flagged_not_fatal():
    result = decode("cZsS")
    assert result["ok"] is True
    f = field(result, "cache lookup for URL")
    assert f["code"] == "Z"
    assert f.get("unknown") is True
    assert field(result, "Response information")["code"] == "S"


@pytest.mark.parametrize("garbage", ["rubbish", "", "12345", "SSSS", "long rubbish via code2"])
def test_garbage_is_rejected(garbage):
    result = decode(garbage)
    assert result["ok"] is False
    assert result["error"]
