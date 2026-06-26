from pydantic import BaseModel, ConfigDict


class HARBaseModel(BaseModel):
    """
    Base class for HAR schemas.

    HAR contains many vendor-specific "_" prefixed fields,
    so allow unknown keys.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)
