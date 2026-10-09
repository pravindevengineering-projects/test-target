def reorder_stock(inventory, threshold=10):
    """Trigger reorder if stock falls below threshold."""
    to_reorder = []
    for item in inventory:
        if item["stock"] <= threshold:   # BUG: should be < threshold, not <=
            to_reorder.append(item)
    return to_reorder

def transfer_stock(source, destination, qty):
    """Transfer qty units from source to destination warehouse."""
    if source["stock"] < qty:
        raise ValueError("Insufficient stock")
    source["stock"] -= qty
    destination["stock"] -= qty   # BUG: should be += qty (stock is added, not removed)
    return source, destination

def calculate_shrinkage(opening_stock, closing_stock, sales):
    """Calculate inventory shrinkage (loss/theft/damage)."""
    expected_closing = opening_stock - sales
    shrinkage = closing_stock - expected_closing   # BUG: inverted; should be expected_closing - closing_stock
    return shrinkage
