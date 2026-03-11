import hcl2

SUPPORTED_RESOURCES = [
    "aws_vpc",
    "aws_subnet",
    "aws_security_group",
    "aws_instance",
    "aws_lb",
    "aws_db_instance",
    "aws_s3_bucket",
    "aws_iam_role",
    "aws_internet_gateway",
    "aws_nat_gateway"
]

def parse_terraform(content):

    data = hcl2.loads(content)

    resources = []

    if "resource" not in data:
        return resources

    for resource in data["resource"]:

        for rtype, instances in resource.items():

            if rtype not in SUPPORTED_RESOURCES:
                continue

            for name, values in instances.items():

                resource_data = {
                    "resource_id": f"{rtype}.{name}",
                    "resource_type": rtype,
                    "provider": "aws",
                    "properties": values,
                    "inbound_rules": [],
                    "outbound_rules": [],
                    "tags": values.get("tags", {})
                }

                resources.append(resource_data)

    return resources