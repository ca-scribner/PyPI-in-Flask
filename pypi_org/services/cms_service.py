fake_db = {
    '/company/history': {  # This could be the primary key of the database
        "page_title": "Company History",  # The fields...
        "page_details": "Details about company history...",
    },
    "/company/employees": {
        "page_title": "Our Team",
        "page_details": "Details about company employees...",
    },
}


def get_page(url: str) -> dict:
    if not url:
        return {}

    url = url.strip().lower()
    url = "/" + url.lstrip("/")

    page = fake_db.get(url, {})
    return page
