
from pathlib import Path
import traceback

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from backend import run_travel_agent


# Project directory
BASE_DIR = Path(__file__).resolve().parent

# FastAPI application
app = FastAPI(
    title="TripMate Travel Planner",
    description="A multi-agent travel planning application.",
    version="1.0.0",
)

# Static files: CSS, JavaScript, images
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

# HTML templates
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# Request model
class TravelRequest(BaseModel):
    user_input: str = Field(
        ...,
        min_length=1,
        description="Travel request from the user",
    )
    thread_id: str | None = None


# Homepage
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


# Travel planning API
@app.post("/api/travel")
async def travel_planner(request_data: TravelRequest):
    try:
        user_message = request_data.user_input.strip()

        if not user_message:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Message cannot be empty.",
                },
            )

        # Run the travel-planning agent
        result = run_travel_agent(
            user_input=user_message,
            thread_id=request_data.thread_id,
        )

        return JSONResponse(
            content={
                "success": True,
                "thread_id": result.get("thread_id"),
                "answer": result.get("answer", ""),
                "flight_results": result.get("flight_results", []),
                "hotel_results": result.get("hotel_results", []),
                "itinerary": result.get("itinerary", {}),
                "llm_calls": result.get("llm_calls", 0),
            }
        )

    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
            },
        )


# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "AI Travel Planner API is running",
    }


# Favicon
@app.get("/favicon.ico")
async def favicon():
    return JSONResponse(content={})


# Start application
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )