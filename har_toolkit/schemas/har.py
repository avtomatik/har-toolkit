from datetime import datetime

from pydantic import Field

from .base import HARBaseModel
from .entry import Entry


class Creator(HARBaseModel):
    name: str
    version: str


class PageTiming(HARBaseModel):
    on_content_load: float | None = Field(default=None, alias="onContentLoad")
    on_load: float | None = Field(default=None, alias="onLoad")


class Page(HARBaseModel):
    started_date_time: datetime | str = Field(alias="startedDateTime")
    id: str
    title: str
    page_timings: PageTiming | None = Field(default=None, alias="pageTimings")


class HARLog(HARBaseModel):
    version: str
    creator: Creator
    pages: list[Page] = Field(default_factory=list)
    entries: list[Entry] = Field(default_factory=list)


class HARFile(HARBaseModel):
    log: HARLog

    def requests(self):
        return [e.request for e in self.log.entries]

    def failed_requests(self):
        return [e for e in self.log.entries if e.response.status >= 400]

    def urls(self):
        return [e.request.url for e in self.log.entries]

    def javascript_responses(self):
        return [
            e.response.content.text
            for e in self.log.entries
            if e.response.content.mime_type == "application/javascript"
        ]
