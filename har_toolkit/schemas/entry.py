from datetime import datetime
from typing import Any

from pydantic import Field

from .base import HARBaseModel


class Cookie(HARBaseModel):
    name: str
    value: str
    path: str | None = None
    domain: str | None = None
    expires: datetime | str | None = None
    http_only: bool | None = Field(default=None, alias="httpOnly")
    secure: bool | None = None


class NameValue(HARBaseModel):
    name: str
    value: str


class PostData(HARBaseModel):
    mime_type: str | None = Field(default=None, alias="mimeType")
    text: str | None = None
    params: list[NameValue] | None = None


class QueryParameter(NameValue): ...


class Request(HARBaseModel):
    method: str
    url: str
    http_version: str | None = Field(default=None, alias="httpVersion")
    headers: list[NameValue] = Field(default_factory=list)
    query_string: list[QueryParameter] = Field(
        default_factory=list, alias="queryString"
    )
    cookies: list[Cookie] = Field(default_factory=list)
    headers_size: int | None = Field(default=None, alias="headersSize")
    body_size: int | None = Field(default=None, alias="bodySize")
    post_data: PostData | None = Field(default=None, alias="postData")


class Content(HARBaseModel):
    size: int | None = None
    mime_type: str | None = Field(default=None, alias="mimeType")
    text: str | None = None
    encoding: str | None = None


class Response(HARBaseModel):
    status: int
    status_text: str | None = Field(default=None, alias="statusText")
    http_version: str | None = Field(default=None, alias="httpVersion")
    headers: list[NameValue] = Field(default_factory=list)
    cookies: list[Cookie] = Field(default_factory=list)
    content: Content = Field(default_factory=Content)
    redirect_url: str | None = Field(default=None, alias="redirectURL")
    headers_size: int | None = Field(default=None, alias="headersSize")
    body_size: int | None = Field(default=None, alias="bodySize")


class Timings(HARBaseModel):
    blocked: float | None = None
    dns: float | None = None
    connect: float | None = None
    send: float | None = None
    wait: float | None = None
    receive: float | None = None
    ssl: float | None = None


class Entry(HARBaseModel):
    started_date_time: datetime | str = Field(alias="startedDateTime")
    time: float
    request: Request
    response: Response
    cache: dict[str, Any] = Field(default_factory=dict)
    timings: Timings
    server_ip_address: str | None = Field(
        default=None, alias="serverIPAddress"
    )
    connection: str | None = None
    page_ref: str | None = Field(default=None, alias="pageref")
