import json
from pathlib import Path

from har_toolkit.schemas.har import HARFile

with Path("some.har").open("r", encoding="utf-8") as f:
    raw_har = json.load(f)

har = HARFile.model_validate(raw_har)

# =============================================================================
# all failed requests
# =============================================================================
failed = [e for e in har.log.entries if e.response.status >= 400]


# =============================================================================
# extract URLs
# =============================================================================
urls = [e.request.url for e in har.log.entries]


# =============================================================================
# find javascript payloads
# =============================================================================
js = [
    e.response.content.text
    for e in har.log.entries
    if e.response.content.mime_type == "application/javascript"
]
