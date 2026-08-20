import json
from dataclasses import dataclass


@dataclass
class License:
    id: str
    customer_id: str
    product: str
    seats: int
    active: bool


if __name__ == "__main__":
    license_json = """
    {
        "id": "L001",
        "customer_id": "C001",
        "product": "Microsoft 365",
        "seats": 100,
        "active": true
    }
    """
    license_data = json.loads(license_json)

    license_info = License(
        id=license_data["id"],
        customer_id=license_data["customer_id"],
        product=license_data["product"],
        seats=license_data["seats"],
        active=license_data["active"],
    )
    print(license_info)

# JSON is a data interchange format.
# dict is a Python data structure.
# License is our domain object.
# license_json（json string） -> dict -> License


@dataclass
class Customer:
    id: str
    name: str
    country: str


def validate_license(customer: Customer, license_info: License) -> bool:
    return (
        license_info.active
        and license_info.seats > 0
        and customer.country == "USA"
        and customer.id == license_info.customer_id
    )


if __name__ == "__main__":
    customer_json = """
    {
        "id": "C001",
        "name": "John Doe",
        "country": "USA"
    }
    """
    customer_data = json.loads(customer_json)
    customer = Customer(
        id=customer_data["id"],
        name=customer_data["name"],
        country=customer_data["country"],
    )
    print(customer)

    result = validate_license(customer, license_info)
    print(result)

    license_info2 = License(
        id="L002", customer_id="C001", product="Windows", seats=0, active=True
    )
    invalid_result = validate_license(customer, license_info2)
    print(invalid_result)
