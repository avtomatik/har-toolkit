import json

from pydantic import TypeAdapter

from har_toolkit.config.paths import FIXTURES_DIR
from har_toolkit.schemas.entry import Entry
from har_toolkit.schemas.har import HARFile


def main() -> None:
    with (FIXTURES_DIR / "actual.har").open("r", encoding="utf-8") as f:
        raw_har = json.load(f)

    har = HARFile.model_validate(raw_har)

    # =========================================================================
    # all failed requests
    # =========================================================================
    failed = har.failed_requests()

    # =========================================================================
    # extract URLs
    # =========================================================================
    urls = har.urls()

    # =========================================================================
    # find javascript payloads
    # =========================================================================
    js = har.javascript_responses()

    print(f"URLs: {urls}")
    print(f"JavaScript Payloads: {js}")

    adapter = TypeAdapter(list[Entry])

    with (FIXTURES_DIR / "failed.json").open("wb") as f:
        f.write(adapter.dump_json(failed, by_alias=True, indent=2))


if __name__ == "__main__":
    main()
