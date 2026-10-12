def build_context(properties):
    context_parts = []

    for _, row in properties.iterrows():
        property_text = (
            f"Property ID: {row['id']}\n"
            f"City: {row['city']}\n"
            f"Location: {row['location']}\n"
            f"Type: {row['house_type']}\n"
            f"Area: {row['house_size']} sq ft\n"
            f"Monthly rent: ₹{row['price']}\n"
            f"Bathrooms: {row['numBathrooms']}\n"
            f"Description: {row['description']}"
        )

        context_parts.append(property_text)

    return "\n\n".join(context_parts)