import numpy as np
import pandas as pd

from app.embeddings.embedder import load_embedding_model
from app.embeddings.text_builder import build_property_text


def build_embeddings(data_path, output_dir):
    df = pd.read_json(data_path, lines=True)

    texts = df.apply(build_property_text, axis=1).tolist()

    model = load_embedding_model()
    embeddings = model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True
    )

    np.save(f"{output_dir}/property_embeddings.npy", embeddings)
    df.to_json(
        f"{output_dir}/properties.jsonl",
        orient="records",
        lines=True
    )

    print("Properties:", len(df))
    print("Embeddings shape:", embeddings.shape)


if __name__ == "__main__":
    build_embeddings(
        "data/processed/properties.jsonl",
        "data/processed"
    )