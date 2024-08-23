from pydantic import BaseModel
from datetime import datetime

class FundDetails(BaseModel):
    id: str
    fund_name: str
    manager_name: str
    desc: str
    net_asset: float
    created_at: datetime
    performance: float