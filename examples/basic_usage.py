import json

from har_toolkit.config.paths import FIXTURES_DIR
from har_toolkit.schemas.har import HARFile


def main() -> None:
    with (FIXTURES_DIR / "actual.har").open("r", encoding="utf-8") as f:
        raw_har = json.load(f)
    har = HARFile.model_validate(raw_har)
    print(f"Total Entries: {len(har.log.entries)}")
    request = har.log.entries[0].request
    print(f"Request HTTP Version: {request.http_version}")
    print(f"Request Query String: {request.query_string}")
    print(f"Request POST Data: {request.post_data}")
    har.model_dump(by_alias=True, exclude_none=True)


if __name__ == "__main__":
    main()
