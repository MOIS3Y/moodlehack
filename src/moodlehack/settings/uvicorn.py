"""Build Uvicorn settings from the installed server's public signature."""

from inspect import Parameter, signature
from typing import TYPE_CHECKING, ClassVar, cast, get_type_hints

from pydantic import BaseModel, ConfigDict, create_model
from uvicorn import run


class _UvicornSettings(BaseModel):
    """Validate server options and retain explicitly configured values."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,
    )

    @property
    def as_dict(self) -> dict[str, object]:
        """Return supplied options, including explicit None values."""
        return self.model_dump(exclude_unset=True)


def _create_uvicorn_settings() -> type[_UvicornSettings]:
    """Derive fields, types and defaults without exposing the ASGI app."""
    annotations: dict[str, object] = get_type_hints(run)
    fields: dict[str, tuple[object, object]] = {}
    for name, parameter in signature(run).parameters.items():
        if name == "app" or parameter.kind not in (
            Parameter.POSITIONAL_OR_KEYWORD,
            Parameter.KEYWORD_ONLY,
        ):
            continue
        default = cast(object, parameter.default)
        fields[name] = (
            annotations[name],
            ... if default is Parameter.empty else default,
        )

    return create_model(
        "UvicornServerSettings",
        __config__=None,
        __base__=_UvicornSettings,
        __module__=__name__,
        __doc__="Options accepted by the installed uvicorn.run function.",
        __validators__=None,
        __cls_kwargs__=None,
        __qualname__=None,
        **fields,
    )


if TYPE_CHECKING:

    class UvicornServerSettings(_UvicornSettings):
        """Static interface; runtime fields come from Uvicorn."""

else:
    UvicornServerSettings = _create_uvicorn_settings()
