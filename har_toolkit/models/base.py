from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class HARBaseModel(BaseModel):
    """
    Base class for HAR models.

    HAR contains many vendor-specific "_" prefixed fields,
    so allow unknown keys.
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )


class NameValue(HARBaseModel):
    name: str
    value: str


class Cookie(HARBaseModel):
    name: str
    value: str

    path: str | None = None
    domain: str | None = None

    expires: datetime | str | None = None

    http_only: bool | None = Field(
        default=None,
        alias="httpOnly",
    )

    secure: bool | None = None


class QueryParameter(NameValue): ...


class PostData(HARBaseModel):
    mime_type: str | None = Field(
        default=None,
        alias="mimeType",
    )

    text: str | None = None

    params: list[NameValue] | None = None


class Request(HARBaseModel):
    method: str
    url: str

    http_version: str | None = Field(
        default=None,
        alias="httpVersion",
    )

    headers: list[NameValue] = Field(default_factory=list)

    query_string: list[QueryParameter] = Field(
        default_factory=list,
        alias="queryString",
    )

    cookies: list[Cookie] = Field(default_factory=list)

    headers_size: int | None = Field(
        default=None,
        alias="headersSize",
    )

    body_size: int | None = Field(
        default=None,
        alias="bodySize",
    )

    post_data: PostData | None = Field(
        default=None,
        alias="postData",
    )


class Content(HARBaseModel):
    size: int | None = None

    mime_type: str | None = Field(
        default=None,
        alias="mimeType",
    )

    text: str | None = None

    encoding: str | None = None


class Response(HARBaseModel):
    status: int

    status_text: str | None = Field(
        default=None,
        alias="statusText",
    )

    http_version: str | None = Field(
        default=None,
        alias="httpVersion",
    )

    headers: list[NameValue] = Field(default_factory=list)

    cookies: list[Cookie] = Field(default_factory=list)

    content: Content = Field(default_factory=Content)

    redirect_url: str | None = Field(
        default=None,
        alias="redirectURL",
    )

    headers_size: int | None = Field(
        default=None,
        alias="headersSize",
    )

    body_size: int | None = Field(
        default=None,
        alias="bodySize",
    )


class Timings(HARBaseModel):
    blocked: float | None = None
    dns: float | None = None
    connect: float | None = None
    send: float | None = None
    wait: float | None = None
    receive: float | None = None
    ssl: float | None = None


class PageTiming(HARBaseModel):
    on_content_load: float | None = Field(
        default=None,
        alias="onContentLoad",
    )

    on_load: float | None = Field(
        default=None,
        alias="onLoad",
    )


class Page(HARBaseModel):
    started_date_time: datetime | str = Field(alias="startedDateTime")

    id: str
    title: str

    page_timings: PageTiming | None = Field(
        default=None,
        alias="pageTimings",
    )


class Entry(HARBaseModel):
    started_date_time: datetime | str = Field(alias="startedDateTime")

    time: float

    request: Request
    response: Response

    cache: dict[str, Any] = Field(default_factory=dict)

    timings: Timings

    server_ip_address: str | None = Field(
        default=None,
        alias="serverIPAddress",
    )

    connection: str | None = None

    page_ref: str | None = Field(
        default=None,
        alias="pageref",
    )


class Creator(HARBaseModel):
    name: str
    version: str


class HARLog(HARBaseModel):
    version: str

    creator: Creator

    pages: list[Page] = Field(default_factory=list)

    entries: list[Entry] = Field(default_factory=list)


class HARFile(HARBaseModel):
    log: HARLog

    def requests(self):
        return [e.request for e in self.log.entries]

    def urls(self):
        return [e.request.url for e in self.log.entries]
