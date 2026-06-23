from src.agent.schema_discovery_agent import (
    SchemaDiscoveryResult
)


def build_schema_context(
    schema: SchemaDiscoveryResult
):

    context = []

    context.append("TABLES:")

    for table in schema.tables:
        context.append(
            f"- {table}"
        )

    context.append("\nMETRICS:")

    for metric in schema.metrics:
        context.append(
            f"- {metric}"
        )

    context.append("\nRELATIONSHIPS:")

    for rel in schema.relationships:
        context.append(
            f"- {rel}"
        )

    return "\n".join(context)