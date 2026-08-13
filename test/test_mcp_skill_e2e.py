"""End-to-end contract tests for the live NotFair MCP-backed skills.

Local registration checks run in the normal suite. Set LIVE_MCP_E2E=1 to also
verify the production endpoint -> 401 challenge -> OAuth resource metadata
round trip without using or exposing an account credential.
"""

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

import pytest


ROOT = Path(__file__).parent.parent

SURFACES = {
    "NotFair-XAds": {
        "endpoint": "https://notfair.co/api/mcp/x_ads",
        "skill": "paid-ads/paid-ads-x",
        "placeholder": "~~x-ads",
    },
    "NotFair-LinkedInAds": {
        "endpoint": "https://notfair.co/api/mcp/linkedin_ads",
        "skill": "paid-ads/paid-ads-linkedin",
        "placeholder": "~~linkedin-ads",
    },
    "NotFair-GoogleSearchConsole": {
        "endpoint": "https://notfair.co/api/mcp/google_search_console",
        "skill": "analytics/search-console",
        "placeholder": "~~search-console",
    },
    "NotFair-GoogleAnalytics": {
        "endpoint": "https://notfair.co/api/mcp/google_analytics",
        "skill": "analytics/google-analytics",
        "placeholder": "~~google-analytics",
    },
}


def test_mcp_surfaces_are_registered_to_corresponding_skills():
    config = json.loads((ROOT / ".mcp.json").read_text())
    plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
    servers = config["mcpServers"]

    for server_name, expected in SURFACES.items():
        assert servers[server_name] == {
            "type": "http",
            "url": expected["endpoint"],
        }

        skill_path = ROOT / expected["skill"] / "SKILL.md"
        assert skill_path.is_file()
        skill_text = skill_path.read_text()
        assert expected["endpoint"] in skill_text
        assert expected["placeholder"] in skill_text
        assert f'./{expected["skill"]}' in plugin["skills"]


@pytest.mark.skipif(
    os.environ.get("LIVE_MCP_E2E") != "1",
    reason="Set LIVE_MCP_E2E=1 to verify production OAuth discovery",
)
@pytest.mark.parametrize("server_name", SURFACES)
def test_live_mcp_oauth_discovery_round_trip(server_name):
    endpoint = SURFACES[server_name]["endpoint"]
    request = urllib.request.Request(
        endpoint,
        headers={"Accept": "application/json, text/event-stream"},
    )

    with pytest.raises(urllib.error.HTTPError) as exc_info:
        urllib.request.urlopen(request, timeout=20)

    response = exc_info.value
    assert response.code == 401
    challenge = response.headers["WWW-Authenticate"]
    match = re.search(r'resource_metadata="([^"]+)"', challenge or "")
    assert match, challenge

    body = json.loads(response.read())
    metadata_url = match.group(1)
    assert body["oauth"]["resource_metadata"] == metadata_url
    assert body["oauth"]["authorization_code_pkce"] is True

    with urllib.request.urlopen(metadata_url, timeout=20) as metadata_response:
        metadata = json.load(metadata_response)

    assert metadata["resource"] == endpoint
    assert "https://notfair.co" in metadata["authorization_servers"]
    assert metadata["resource_name"].startswith("NotFair ")
