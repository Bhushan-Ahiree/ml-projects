def build_property_text(row) -> str:
    return (
        f"Property type: {row['house_type']}. "
        f"Location: {row['location']}, {row['city']}. "
        f"Area: {row['house_size']} sq ft. "
        f"Monthly rent: {row['price']}. "
        f"Bathrooms: {row['numBathrooms']}. "
        f"Description: {row['description']}"
    )