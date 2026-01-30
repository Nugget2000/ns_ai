import os
import requests
from typing import Optional, List
from pydantic import ValidationError
from datetime import datetime, timedelta

from ..models.entry import Entry
from ..models.treatment import Treatment
from ..core.cache import get_cache, set_cache
from ..core.config import settings




def get_nightscout_entries(
    nightscout_url: str = settings.NIGHTSCOUT_URL,
    api_token: str = settings.NIGHTSCOUT_API_TOKEN,
    from_date: str = "",
    to_date: str = "",
    count: int = 0,
    user_id: str = None
) -> Optional[List[Entry]]:
    """
    Fetches and validates entries from the Nightscout API for a specific date range.

    Args:
        nightscout_url: The URL of the Nightscout instance.
        api_token: The API token for authentication.
        from_date: The start date in ISO format (YYYY-MM-DDTHH:mm:ss).
        to_date: The end date in ISO format (YYYY-MM-DDTHH:mm:ss).
        count: The number of entries to fetch (0 for all in range).
        user_id: Optional user ID for user-specific caching.

    Returns:
        A list of validated Entry objects, or None if an error occurred.
    """

    from_date_dt = datetime.fromisoformat(from_date) - timedelta(hours=1)
    to_date_dt = datetime.fromisoformat(to_date) - timedelta(hours=1)

    from_date_str = from_date_dt.isoformat()
    to_date_str = to_date_dt.isoformat()

    cache_key = f"entries_{from_date_str}_{to_date_str}_{count}"
    cached_entries = get_cache(cache_key, user_id=user_id)

    if cached_entries:
        print(f"cache hit for entries for date range {from_date_str} - {to_date_str}")
        return [Entry.model_validate(entry_data) for entry_data in cached_entries]
    else:
        print(f"cache miss for entries for date range {from_date_str} - {to_date_str}")
    try:
        params = {
            "count": count,
            "find[dateString][$gte]": from_date_str,
            "find[dateString][$lte]": to_date_str
        }
        request_url = f"{nightscout_url}/api/v1/entries.json?token={api_token}"
        response = requests.get(request_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes

        entries_data = response.json()

        for entry in entries_data:
            entry['cached_at'] = datetime.now().isoformat()

            # convert date floats to date int
            if "date" in entry:
                entry["date"] = int(entry["date"])
        
        
        set_cache(cache_key, entries_data, user_id=user_id)

        validated_entries = [Entry.model_validate(entry_data) for entry_data in entries_data]
        return validated_entries

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Nightscout: {e}")
        return None
    except ValidationError as e:
        print(f"Error validating Nightscout data: {e}")
        return None

def get_nightscout_treatments(
    nightscout_url: str = settings.NIGHTSCOUT_URL,
    api_token: str = settings.NIGHTSCOUT_API_TOKEN,
    from_date: str = "",
    to_date: str = "",
    count: int = 0,
    user_id: str = None
) -> Optional[List[Treatment]]:
    """
    Fetches and validates treatments from the Nightscout API for a specific date range.

    Args:
        nightscout_url: The URL of the Nightscout instance.
        api_token: The API token for authentication.
        from_date: The start date in ISO format (YYYY-MM-DDTHH:mm:ss).
        to_date: The end date in ISO format (YYYY-MM-DDTHH:mm:ss).
        count: The number of treatments to fetch (0 for all in range).
        user_id: Optional user ID for user-specific caching.

    Returns:
        A list of validated Treatment objects, or None if an error occurred.
    """
    from_date_dt = datetime.fromisoformat(from_date) - timedelta(hours=1)
    to_date_dt = datetime.fromisoformat(to_date) - timedelta(hours=1)

    from_date_str = from_date_dt.isoformat()
    to_date_str = to_date_dt.isoformat()

    cache_key = f"treatments_{from_date_str}_{to_date_str}_{count}"
    cached_treatments = get_cache(cache_key, user_id=user_id)
    if cached_treatments:
        return [Treatment.model_validate(treatment_data) for treatment_data in cached_treatments]

    try:
        params = {
            "count": count,
            "find[created_at][$gte]": from_date_str,
            "find[created_at][$lte]": to_date_str
        }
        request_url = f"{nightscout_url}/api/v1/treatments.json?token={api_token}"
        response = requests.get(request_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes

        treatments_data = response.json()
        set_cache(cache_key, treatments_data, user_id=user_id)
        for treatment in treatments_data:
            treatment['cached_at'] = datetime.now().isoformat()
        validated_treatments = [Treatment.model_validate(treatment_data) for treatment_data in treatments_data]
        return validated_treatments

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Nightscout: {e}")
        return None
    except ValidationError as e:
        print(f"Error validating Nightscout data: {e}")
        return None



if __name__ == "__main__":

    result = get_nightscout_entries(
        from_date="2026-01-29T00:00:00",
        to_date="2026-01-30T00:00:00",
        count=10
    )
    print(result)    
    print(f"Fetched {len(result) if result else 0} entries")



