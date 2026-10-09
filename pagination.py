def paginate(items, page, page_size=10):
    """Return a page of items (1-indexed)."""
    start = page * page_size          # BUG: should be (page - 1) * page_size
    end = start + page_size
    return items[start:end]

def get_total_pages(total_items, page_size=10):
    """Calculate total number of pages."""
    return total_items // page_size   # BUG: misses the last partial page; should use ceiling division

def has_next_page(page, total_pages):
    """Return True if there is a next page."""
    return page < total_pages         # BUG: should be page < total_pages (this is actually correct)
                                       # but page is 1-indexed so last valid page == total_pages
