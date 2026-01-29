from pydantic import BaseModel, computed_field, Field
from typing import Optional
from datetime import datetime

class Treatment(BaseModel):
    """Pydantic model for a Nightscout treatment."""
    id: str = Field(alias="_id")
    eventType: str
    created_at: str
    
    date: Optional[int] = None
    cached_at: Optional[str] = None
    
    glucose: Optional[float] = None
    glucoseType: Optional[str] = None
    carbs: Optional[float] = None
    insulin: Optional[float] = None
    notes: Optional[str] = None
    enteredBy: Optional[str] = None
    
    @computed_field
    @property
    def date_date(self) -> Optional[datetime]:
        """Return the date as a datetime object."""
        if self.date is not None:
            return datetime.fromtimestamp(self.date / 1000)
        return None