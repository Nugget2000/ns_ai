"""
Data Analysis Service for Nightscout data.

This module provides the DayData class for storing and analyzing
a full day of Nightscout data including entries and treatments.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Literal
import statistics
import math

# Conversion factor: mg/dL to mmol/L
MGDL_TO_MMOL = 18.0

from ..models.entry import Entry
from ..models.treatment import Treatment
from .nightscout_service import get_nightscout_entries, get_nightscout_treatments


@dataclass
class EntryInsights:
    """Insights calculated from glucose entries."""
    
    # Unit used for glucose values
    unit: Literal["mg/dL", "mmol/L"]
    
    # Core statistics
    mean: float
    median: float
    standard_deviation: float
    cv: float  # Coefficient of Variation (%)
    
    # Time in Range metrics (in minutes)
    tir_minutes: int  # Time in range (70-180 mg/dL or 3.9-10 mmol/L)
    tir_percentage: float
    tbr_minutes: int  # Time below range (<70 mg/dL or <3.9 mmol/L)
    tbr_percentage: float
    tar_minutes: int  # Time above range (>180 mg/dL or >10 mmol/L)
    tar_percentage: float
    titr_minutes: int  # Time in tight range (70-140 mg/dL or 3.9-7.8 mmol/L)
    titr_percentage: float
    
    # Additional metrics
    estimated_hba1c: float  # Estimated HbA1c based on average glucose
    total_reading_count: int
    
    # Min/Max
    min_glucose: float
    max_glucose: float
    
    # Range thresholds used (for display purposes)
    low_threshold: float
    high_threshold: float
    tight_high_threshold: float


@dataclass
class DayData:
    """
    Container for a full day of Nightscout data with analysis capabilities.
    
    This class stores raw entries and treatments for a specific date and
    provides methods to extract various insights from the data.
    """
    
    date: datetime
    entries: List[Entry] = field(default_factory=list)
    treatments: List[Treatment] = field(default_factory=list)
    
    # Standard range values in mg/dL
    LOW_THRESHOLD: int = 70  # 3.9 mmol/L
    HIGH_THRESHOLD: int = 180  # 10 mmol/L
    TIGHT_HIGH_THRESHOLD: int = 140  # 7.8 mmol/L
    
    # Reading interval (CGM readings typically every 5 minutes)
    READING_INTERVAL_MINUTES: int = 5
    
    def get_glucose_values(self) -> List[int]:
        """Extract all valid sgv (glucose) values from entries."""
        return [entry.sgv for entry in self.entries if entry.sgv is not None]
    
    def calculate_entry_insights(self, use_mmol: bool = False) -> Optional[EntryInsights]:
        """
        Calculate all insights from the glucose entries.
        
        Args:
            use_mmol: If True, return values in mmol/L; otherwise mg/dL.
        
        Returns:
            EntryInsights object with all calculated metrics, or None if no valid data.
        """
        glucose_values = self.get_glucose_values()
        
        if not glucose_values:
            return None
        
        total_readings = len(glucose_values)
        
        # Core statistics (calculated in mg/dL first)
        mean_glucose = statistics.mean(glucose_values)
        median_glucose = statistics.median(glucose_values)
        
        # Standard deviation (need at least 2 values)
        if total_readings >= 2:
            std_dev = statistics.stdev(glucose_values)
        else:
            std_dev = 0.0
        
        # Coefficient of Variation (CV) = (StdDev / Mean) * 100
        # CV is unitless percentage, same regardless of unit
        cv = (std_dev / mean_glucose * 100) if mean_glucose > 0 else 0.0
        
        # Time in Range calculations (always use mg/dL thresholds for calculation)
        tir_count = sum(1 for v in glucose_values 
                        if self.LOW_THRESHOLD <= v <= self.HIGH_THRESHOLD)
        tbr_count = sum(1 for v in glucose_values 
                        if v < self.LOW_THRESHOLD)
        tar_count = sum(1 for v in glucose_values 
                        if v > self.HIGH_THRESHOLD)
        titr_count = sum(1 for v in glucose_values 
                         if self.LOW_THRESHOLD <= v <= self.TIGHT_HIGH_THRESHOLD)
        
        # Convert counts to minutes (assuming 5-minute intervals)
        tir_minutes = tir_count * self.READING_INTERVAL_MINUTES
        tbr_minutes = tbr_count * self.READING_INTERVAL_MINUTES
        tar_minutes = tar_count * self.READING_INTERVAL_MINUTES
        titr_minutes = titr_count * self.READING_INTERVAL_MINUTES
        
        # Calculate percentages
        tir_percentage = (tir_count / total_readings * 100) if total_readings > 0 else 0.0
        tbr_percentage = (tbr_count / total_readings * 100) if total_readings > 0 else 0.0
        tar_percentage = (tar_count / total_readings * 100) if total_readings > 0 else 0.0
        titr_percentage = (titr_count / total_readings * 100) if total_readings > 0 else 0.0
        
        # Estimated HbA1c
        # Formula: eHbA1c = (mean_glucose + 46.7) / 28.7 (ADAG study)
        # This uses mg/dL
        estimated_hba1c = (mean_glucose + 46.7) / 28.7
        
        # Min/Max
        min_glucose_val = min(glucose_values)
        max_glucose_val = max(glucose_values)
        
        # Convert to mmol/L if requested
        if use_mmol:
            unit = "mmol/L"
            mean_glucose = mean_glucose / MGDL_TO_MMOL
            median_glucose = median_glucose / MGDL_TO_MMOL
            std_dev = std_dev / MGDL_TO_MMOL
            min_glucose_val = min_glucose_val / MGDL_TO_MMOL
            max_glucose_val = max_glucose_val / MGDL_TO_MMOL
            low_threshold = self.LOW_THRESHOLD / MGDL_TO_MMOL
            high_threshold = self.HIGH_THRESHOLD / MGDL_TO_MMOL
            tight_high_threshold = self.TIGHT_HIGH_THRESHOLD / MGDL_TO_MMOL
        else:
            unit = "mg/dL"
            low_threshold = float(self.LOW_THRESHOLD)
            high_threshold = float(self.HIGH_THRESHOLD)
            tight_high_threshold = float(self.TIGHT_HIGH_THRESHOLD)
        
        return EntryInsights(
            unit=unit,
            mean=round(mean_glucose, 1),
            median=round(median_glucose, 1),
            standard_deviation=round(std_dev, 1),
            cv=round(cv, 1),
            tir_minutes=tir_minutes,
            tir_percentage=round(tir_percentage, 1),
            tbr_minutes=tbr_minutes,
            tbr_percentage=round(tbr_percentage, 1),
            tar_minutes=tar_minutes,
            tar_percentage=round(tar_percentage, 1),
            titr_minutes=titr_minutes,
            titr_percentage=round(titr_percentage, 1),
            estimated_hba1c=round(estimated_hba1c, 1),
            total_reading_count=total_readings,
            min_glucose=round(min_glucose_val, 1),
            max_glucose=round(max_glucose_val, 1),
            low_threshold=round(low_threshold, 1),
            high_threshold=round(high_threshold, 1),
            tight_high_threshold=round(tight_high_threshold, 1)
        )


def get_day_data(
    date: datetime,
    nightscout_url: Optional[str] = None,
    api_token: Optional[str] = None
) -> Optional[DayData]:
    """
    Fetch a full day of data from Nightscout and return a DayData object.
    
    Args:
        date: The date to fetch data for (time component is ignored).
        nightscout_url: Optional Nightscout URL (uses settings if not provided).
        api_token: Optional API token (uses settings if not provided).
    
    Returns:
        DayData object populated with entries and treatments, or None on error.
    """
    # Create date range for the full day
    start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0)
    end_of_day = start_of_day + timedelta(days=1)
    
    from_date_str = start_of_day.isoformat()
    to_date_str = end_of_day.isoformat()
    
    # Fetch entries
    kwargs = {}
    if nightscout_url:
        kwargs['nightscout_url'] = nightscout_url
    if api_token:
        kwargs['api_token'] = api_token
    
    entries = get_nightscout_entries(
        from_date=from_date_str,
        to_date=to_date_str,
        count=0,  # Get all entries
        **kwargs
    )
    
    treatments = get_nightscout_treatments(
        from_date=from_date_str,
        to_date=to_date_str,
        count=0,  # Get all treatments
        **kwargs
    )
    
    if entries is None and treatments is None:
        return None
    
    return DayData(
        date=start_of_day,
        entries=entries or [],
        treatments=treatments or []
    )


def print_insights(insights: EntryInsights) -> None:
    """Helper function to print insights."""
    unit = insights.unit
    print(f"\n=== Entry Insights ({unit}) ===")
    print(f"Total Readings: {insights.total_reading_count}")
    print(f"Mean Glucose: {insights.mean} {unit}")
    print(f"Median Glucose: {insights.median} {unit}")
    print(f"Standard Deviation: {insights.standard_deviation} {unit}")
    print(f"Coefficient of Variation: {insights.cv}%")
    print(f"Min Glucose: {insights.min_glucose} {unit}")
    print(f"Max Glucose: {insights.max_glucose} {unit}")
    print(f"\nTime in Range ({insights.low_threshold}-{insights.high_threshold}): {insights.tir_minutes} min ({insights.tir_percentage}%)")
    print(f"Time Below Range (<{insights.low_threshold}): {insights.tbr_minutes} min ({insights.tbr_percentage}%)")
    print(f"Time Above Range (>{insights.high_threshold}): {insights.tar_minutes} min ({insights.tar_percentage}%)")
    print(f"Time in Tight Range ({insights.low_threshold}-{insights.tight_high_threshold}): {insights.titr_minutes} min ({insights.titr_percentage}%)")
    print(f"\nEstimated HbA1c: {insights.estimated_hba1c}%")


if __name__ == "__main__":
    # Test the data analysis service
    test_date = datetime(2026, 1, 29)
    
    print(f"Fetching data for {test_date.date()}...")
    day_data = get_day_data(test_date)
    
    if day_data:
        print(f"Fetched {len(day_data.entries)} entries and {len(day_data.treatments)} treatments")
        
        # Show insights in mg/dL
        insights_mgdl = day_data.calculate_entry_insights(use_mmol=False)
        if insights_mgdl:
            print_insights(insights_mgdl)
        
        # Show insights in mmol/L
        insights_mmol = day_data.calculate_entry_insights(use_mmol=True)
        if insights_mmol:
            print_insights(insights_mmol)
        
        if not insights_mgdl:
            print("No glucose readings found for insights calculation")
    else:
        print("Failed to fetch day data")
