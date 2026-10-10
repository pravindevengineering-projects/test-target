def calculate_total(items, coupon_discount=0):
    """Calculate cart total after discount."""
    subtotal = sum(item["price"] * item["qty"] for item in items)
    discount = subtotal * coupon_discount
    return subtotal - discount  # BUG: coupon_discount is already a fraction (e.g. 0.1),
                                 # but should be divided by 100 if passed as percentage

def apply_bulk_discount(items, threshold=5):
    """Apply 10% discount if more than threshold items."""
    total_qty = sum(item["qty"] for item in items)
    if total_qty > threshold:  # BUG: should be >= threshold, off-by-one
        for item in items:
            item["price"] = item["price"] * 0.9
    return items

def find_most_expensive(items):
    """Return the most expensive item."""
    if not items:
        return None
    most_expensive = items[0]
    for item in items[1:]:
        if item["price"] < most_expensive["price"]:  # BUG: < should be >
            most_expensive = item
    return most_expensive
