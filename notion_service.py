import os

from dotenv import load_dotenv
from notion_client import APIResponseError, Client

load_dotenv()


class NotionAuthError(Exception):
    pass


class NotionDatabaseNotFoundError(Exception):
    pass


class NotionRateLimitError(Exception):
    pass


def _get_client() -> tuple[Client, str]:
    api_key = os.environ.get("NOTION_API_KEY")
    database_id = os.environ.get("NOTION_DATABASE_ID")
    if not api_key:
        raise NotionAuthError("NOTION_API_KEY environment variable is not set")
    if not database_id:
        raise NotionDatabaseNotFoundError(
            "NOTION_DATABASE_ID environment variable is not set"
        )
    return Client(auth=api_key), database_id


def create_application(
    title: str, company: str, url: str, source: str, raw_text: str
) -> str:
    client, database_id = _get_client()

    try:
        page = client.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {"title": [{"text": {"content": title}}]},
                "Company": {"rich_text": [{"text": {"content": company}}]},
                "URL": {"url": url},
                "Source": {"select": {"name": source}},
            },
        )
    except APIResponseError as e:
        if e.status == 401:
            raise NotionAuthError(
                "Invalid Notion API key — check NOTION_API_KEY"
            ) from e
        if e.status == 404:
            raise NotionDatabaseNotFoundError(
                "Database not found — make sure it is shared with your integration"
            ) from e
        if e.status == 429:
            raise NotionRateLimitError("Notion rate limit exceeded — try again later") from e
        raise

    page_id = page["id"]

    client.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": raw_text}}]
                },
            }
        ],
    )

    return page_id
