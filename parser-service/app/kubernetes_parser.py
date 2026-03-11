import yaml

SUPPORTED_K8S = [
    "Service",
    "Deployment",
    "Ingress",
    "NetworkPolicy",
    "ConfigMap",
    "Namespace",
    "ServiceAccount"
]

def parse_kubernetes(content):

    docs = yaml.safe_load_all(content)

    resources = []

    for doc in docs:

        if not doc:
            continue

        kind = doc.get("kind")

        if kind not in SUPPORTED_K8S:
            continue

        metadata = doc.get("metadata", {})

        resources.append({
            "resource_id": metadata.get("name"),
            "resource_type": kind,
            "provider": "kubernetes",
            "properties": doc.get("spec", {}),
            "inbound_rules": [],
            "outbound_rules": [],
            "tags": metadata.get("labels", {})
        })

    return resources