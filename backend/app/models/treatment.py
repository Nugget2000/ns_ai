from pydantic import BaseModel, computed_field, Field
from typing import Optional
from datetime import datetime

class Treatment(BaseModel):
    """Pydantic model for a Nightscout treatment."""
    id: str = Field(alias="_id")
    eventType: str
    created_at: str
    
    date: int
    cached_at: str
    
    glucose: Optional[float] = None
    glucoseType: Optional[str] = None
    carbs: Optional[float] = None
    insulin: Optional[float] = None
    notes: Optional[str] = None
    enteredBy: Optional[str] = None
    
    @computed_field
    @property
    def date_date(self) -> datetime:
        """Return the date as a datetime object."""
        return datetime.fromtimestamp(self.date / 1000)