from pathlib import Path
import yaml

from src.rag.chunker import TextChunker


ASSET_COLLECTIONS = {
    "assets/schema": "schema_docs",
    "assets/metrics": "metric_defs",
    "assets/rules": "business_rules",
    "assets/templates/query_templates": "query_templates",
    "assets/templates/narrative_templates": "narrative_templates",
    "assets/eval": "evaluation_docs",
}


def infer_domain(filename: str):

    filename = filename.lower()

    if any(
        x in filename
        for x in [
            "customer",
            "rfm",
            "segment",
            "champion"
        ]
    ):
        return "customer"

    if any(
        x in filename
        for x in [
            "product",
            "inventory"
        ]
    ):
        return "product"

    if any(
        x in filename
        for x in [
            "revenue",
            "growth",
            "yoy"
        ]
    ):
        return "revenue"

    if any(
        x in filename
        for x in [
            "forecast",
            "prediction"
        ]
    ):
        return "forecast"

    if any(
        x in filename
        for x in [
            "anomaly",
            "outlier"
        ]
    ):
        return "anomaly"

    return "general"


def _yaml_to_text(data):

    if isinstance(data, dict):

        parts = []

        for key, value in data.items():

            if isinstance(value, (dict, list)):

                parts.append(
                    f"{key}: {yaml.dump(value, sort_keys=False)}"
                )

            else:

                parts.append(
                    f"{key}: {value}"
                )

        return "\n".join(parts)

    return str(data)


def load_markdown_documents(base_path):

    documents = []

    path = Path(base_path)

    if not path.exists():
        return documents

    chunker = TextChunker()

    for md_file in path.rglob("*.md"):

        try:

            with open(
                md_file,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read()

            chunks = chunker.chunk_text(content)

            for idx, chunk in enumerate(chunks):

                documents.append(
                    {
                        "content": chunk,
                        "metadata": {
                            "collection": "knowledge_base",
                            "source_file": md_file.name,
                            "file_type": "markdown",
                            "domain": infer_domain(
                                md_file.name
                            ),
                            "chunk_id": idx,
                            "priority": 10
                        }
                    }
                )

        except Exception as e:

            print(
                f"Failed loading markdown file: {md_file} | {e}"
            )

    return documents


def load_sql_documents(base_path):

    documents = []

    path = Path(base_path)

    if not path.exists():
        return documents

    chunker = TextChunker()

    for sql_file in path.rglob("*.sql"):

        try:

            with open(
                sql_file,
                "r",
                encoding="utf-8"
            ) as f:

                content = f.read()

            chunks = chunker.chunk_text(content)

            for idx, chunk in enumerate(chunks):

                documents.append(
                    {
                        "content": chunk,
                        "metadata": {
                            "collection": "sql_library",
                            "source_file": sql_file.name,
                            "file_type": "sql",
                            "domain": infer_domain(
                                sql_file.name
                            ),
                            "chunk_id": idx,
                            "priority": 5
                        }
                    }
                )

        except Exception as e:

            print(
                f"Failed loading sql file: {sql_file} | {e}"
            )

    return documents


def load_yaml_assets():

    documents = []

    for asset_dir, collection_name in ASSET_COLLECTIONS.items():

        path = Path(asset_dir)

        if not path.exists():
            continue

        for yaml_file in path.glob("*.yaml"):

            try:

                with open(
                    yaml_file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    data = yaml.safe_load(f)

                documents.append(
                    {
                        "content": _yaml_to_text(data),
                        "metadata": {
                            "collection": collection_name,
                            "source_file": yaml_file.name,
                            "file_type": "yaml",
                            "domain": infer_domain(
                                yaml_file.name
                            ),
                            "priority": 1
                        }
                    }
                )

            except Exception as e:

                print(
                    f"Failed loading yaml file: {yaml_file} | {e}"
                )

    return documents


def load_all_assets():

    documents = []

    documents.extend(
        load_yaml_assets()
    )

    documents.extend(
        load_markdown_documents(
            "knowledge_base"
        )
    )

    documents.extend(
        load_sql_documents(
            "sql"
        )
    )

    print(
        f"Loaded {len(documents)} total knowledge assets."
    )

    return documents