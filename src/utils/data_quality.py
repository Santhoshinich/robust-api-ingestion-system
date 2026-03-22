import logging


def validate_not_empty(data, endpoint_name):
    if not data:
        raise ValueError(f"{endpoint_name}: No data received")


def validate_required_fields(data, fields, endpoint_name):
    for i, record in enumerate(data):
        for field in fields:
            if field not in record:
                raise ValueError(
                    f"{endpoint_name}: Missing field '{field}' in record {i}"
                )


def validate_record_count(data, min_count, endpoint_name):
    if len(data) < min_count:
        raise ValueError(
            f"{endpoint_name}: Expected at least {min_count} records, got {len(data)}"
        )


def run_checks(data, endpoint_name):
    import logging

    logging.info(f"Running data quality checks for {endpoint_name}")

    validate_not_empty(data, endpoint_name)

    # REST endpoints
    if endpoint_name in ["posts", "comments", "users"]:
        validate_required_fields(data, ["id"], endpoint_name)
        validate_record_count(data, 1, endpoint_name)

    # SOAP endpoint
    elif endpoint_name == "calculator":
        if not isinstance(data, list):
            raise ValueError("calculator: Expected list response")

        for i, record in enumerate(data):
            if "AddResult" not in record:
                raise ValueError(
                    f"calculator: Missing AddResult in record {i}"
                )

    logging.info(f"Data quality checks passed for {endpoint_name}")