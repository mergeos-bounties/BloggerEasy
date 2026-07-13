from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class NavLink(BaseModel):
    model_config = ConfigDict(extra="allow")

    label: str = "Link"
    href: str = "#"

    @field_validator("label", "href", mode="before")
    @classmethod
    def _stringify(cls, value: Any) -> str:
        if value is None:
            return ""
        return str(value).strip()


class ColorPalette(BaseModel):
    model_config = ConfigDict(extra="allow")

    primary: str = "#1a73e8"
    secondary: str = "#34a853"
    background: str = "#ffffff"
    text: str = "#222222"
    palette: list[str] = Field(default_factory=list)

    @field_validator("primary", "secondary", "background", "text", mode="before")
    @classmethod
    def _non_empty_color(cls, value: Any) -> str:
        text = str(value or "").strip()
        return text or "#1a73e8"


class FontSet(BaseModel):
    model_config = ConfigDict(extra="allow")

    body: str = "system-ui, sans-serif"
    heading: str | None = None

    @field_validator("body", "heading", mode="before")
    @classmethod
    def _stringify(cls, value: Any) -> str | None:
        if value is None:
            return None
        return str(value).strip() or None


class FeatureFlags(BaseModel):
    model_config = ConfigDict(extra="allow")

    header: bool = False
    sidebar: bool = False
    footer: bool = False
    dense: bool = False
    nav_count: int = 0


class PageStructure(BaseModel):
    model_config = ConfigDict(extra="allow")

    source: str = "inline"
    title: str = "My Blog"
    description: str = ""
    nav_links: list[NavLink] = Field(default_factory=list)
    headings: list[str] = Field(default_factory=list)
    sample_paragraphs: list[str] = Field(default_factory=list)
    colors: ColorPalette = Field(default_factory=ColorPalette)
    fonts: FontSet = Field(default_factory=FontSet)
    layout: Literal["single-column", "two-column", "three-column"] = "single-column"
    features: FeatureFlags = Field(default_factory=FeatureFlags)
    template: str | None = None
    normalize: dict[str, Any] | None = None

    @field_validator("title", mode="before")
    @classmethod
    def _default_title(cls, value: Any) -> str:
        title = str(value or "").strip()
        return title or "My Blog"

    @field_validator("description", "source", mode="before")
    @classmethod
    def _stringify(cls, value: Any) -> str:
        return str(value or "").strip()

    @field_validator("headings", "sample_paragraphs", mode="before")
    @classmethod
    def _string_list(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if not isinstance(value, list):
            value = [value]
        return [str(item).strip() for item in value if str(item).strip()]


def validate_structure(structure: PageStructure | dict[str, Any]) -> PageStructure:
    if isinstance(structure, PageStructure):
        return structure
    return PageStructure.model_validate(structure or {})


def structure_dict(structure: PageStructure | dict[str, Any]) -> dict[str, Any]:
    return validate_structure(structure).model_dump(exclude_none=True)
