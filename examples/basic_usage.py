import json
from pathlib import Path

from har_toolkit.schemas.har import HARFile

with Path("some.har").open("r", encoding="utf-8") as f:
    raw_har = json.load(f)

har = HARFile.model_validate(raw_har)

print(len(har.log.entries))

request = har.log.entries[0].request

print(request.http_version)
print(request.query_string)
print(request.post_data)

har_json = har.model_dump(by_alias=True, exclude_none=True)
