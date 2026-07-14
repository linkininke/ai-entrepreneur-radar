from pydantic import BaseModel


class StatsResponse(BaseModel):
    sources: int = 0
    information: int = 0
    analyses: int = 0
    opportunities: int = 0
    pending_analysis: int = 0
    pending_opportunities: int = 0
