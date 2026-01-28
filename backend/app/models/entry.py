from pydantic import BaseModel, computed_field, Field
from typing import Optional
from datetime import datetime

class Entry(BaseModel):
    """Pydantic model for a Nightscout entry."""
    id: str = Field(alias="_id")
    type: str
    
    date: int
    dateString: str
    cached_at: str
    sgv: Optional[int] = None
    trend: Optional[int] = None
    direction: Optional[str] = None
    device: str
    utcOffset: int
    sysTime: str
    # mills: int
    
    @computed_field
    @property
    def mmol(self) -> float:
        """Return sgv converted to mmol/L (sgv / 18), rounded to one decimal."""
        if self.sgv is not None:
            return round(self.sgv / 18, 1)
        return None

    @computed_field
    @property
    def date_date(self) -> datetime:
        """Return the date as a datetime object."""
        return datetime.fromtimestamp(self.date / 1000)