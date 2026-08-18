from notion_service import create_application

page_id = create_application(
    title="TEST - delete me",
    company="Test Co",
    url="https://example.com",
    source="Other",
    raw_text="Sample raw text for testing purposes.",
)

print(f"Page created successfully! ID: {page_id}")
