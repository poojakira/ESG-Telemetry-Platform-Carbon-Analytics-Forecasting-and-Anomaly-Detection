from fastapi import APIRouter, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from app.db import get_db, Ledger # type: ignore
from app.auth import get_current_user # type: ignore
from app.recommender import recommender # type: ignore
from app.schemas import RecommendationOutput # type: ignore
from datetime import datetime
import pandas as pd # type: ignore

router = APIRouter(prefix="/recommendations", tags=["Sustainability Action Center"])

@router.get("/", response_model=RecommendationOutput)
def get_sustainability_actions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """ Generates real-time sustainability optimization suggestions. """
    try:
        # 1. Fetch current metrics (similar to metrics endpoint logic)
        items = db.query(Ledger).limit(100).all()
        if not items:
            return {
                "recommendations": [],
                "overall_sustainability_index": 0.0,
                "timestamp": datetime.now().isoformat()
            }
        
        df = pd.DataFrame([vars(i) for i in items])
        metrics = {
            "avg_intensity": float(df['total_lifecycle_carbon_footprint'].mean()),
            "region_breakdown": df['region'].value_counts().to_dict()
        }

        # 2. Get recommendations from engine
        actions = recommender.generate_recommendations(metrics)
        index = recommender.calculate_sustainability_index(metrics)

        return {
            "recommendations": actions,
            "overall_sustainability_index": index,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommender fault: {str(e)}")
