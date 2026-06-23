from src.agent.schema_discovery_agent import (
    SchemaDiscoveryAgent
)

agent = SchemaDiscoveryAgent()

result = agent.discover()

print("\nTABLES")
print("=" * 80)

for t in result.tables:
    print(t)

print("\nCOLUMNS")
print("=" * 80)

for table, cols in result.columns.items():

    print(f"\n{table}")

    for c in cols:
        print("  -", c)

print("\nMETRICS")
print("=" * 80)

for m in result.metrics:
    print(m)

print("\nRELATIONSHIPS")
print("=" * 80)

for r in result.relationships:
    print(r)