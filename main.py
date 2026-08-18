import os
from urllib.parse import urlparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from notion_service import (
    NotionAuthError,
    NotionDatabaseNotFoundError,
    NotionRateLimitError,
    create_application,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CaptureRequest(BaseModel):
    text: str
    url: str
    title: str = "Untitled"


SOURCE_RULES: dict[str, str] = {
    "linkedin.com": "LinkedIn",
    "naukri.com": "Naukri",
}


def _detect_source(url: str) -> str:
    hostname = urlparse(url).hostname or ""
    for domain, source in SOURCE_RULES.items():
        if hostname == domain or hostname.endswith("." + domain):
            return source
    return "Other"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/capture", status_code=201)
def capture(req: CaptureRequest):
    source = _detect_source(req.url)
    try:
        page_id = create_application(
            title=req.title,
            company="",
            url=req.url,
            source=source,
            raw_text=req.text,
        )
    except (NotionAuthError, NotionDatabaseNotFoundError) as e:
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e)}
        )
    except NotionRateLimitError as e:
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"success": False, "error": str(e)}
        )

    return {"success": True, "page_id": page_id, "message": "Saved to Notion"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
