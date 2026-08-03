from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import sys
import os
import requests
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db
from models import User
from auth import get_current_user
from config import CANLII_API_KEY

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/canlii")
async def search_canlii(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search CanLII (Canadian legal database) for case law"""
    if not query or len(query.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")

    try:
        base_url = "https://canlii.org/api/v1"

        if CANLII_API_KEY:
            params = {
                "q": query,
                "api_key": CANLII_API_KEY,
                "language": "en"
            }
            response = requests.get(f"{base_url}/search", params=params, timeout=10)
        else:
            params = {
                "q": query,
                "language": "en"
            }
            response = requests.get(f"{base_url}/search", params=params, timeout=10)

        response.raise_for_status()
        results = response.json()

        formatted_results = []
        if "results" in results:
            for result in results["results"][:20]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "citation": result.get("citation", ""),
                    "url": result.get("url", ""),
                    "relevance": result.get("relevance", 0),
                    "judge": result.get("judge", ""),
                    "date": result.get("date", ""),
                    "summary": result.get("summary", "")[:500]
                })

        return {
            "query": query,
            "count": len(formatted_results),
            "results": formatted_results
        }

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="CanLII search timed out")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error searching CanLII: {str(e)}")

@router.get("/google-scholar")
async def search_google_scholar(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fallback search using a free legal search service"""
    if not query or len(query.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")

    try:
        base_url = "https://scholar.google.com/scholar"

        params = {
            "q": query,
            "hl": "en",
            "as_sdt": ",5"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        return {
            "query": query,
            "note": "Google Scholar search available but requires parsing HTML. Use CanLII for better API integration.",
            "url": response.url
        }

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Search timed out")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error searching: {str(e)}")
