customer = {
    "id": "C001",
    "name": "John Doe",
    "country": "USA",
}

# list, can be list[dict]
customers = [
    {
        "id": "C001",
        "name": "John Doe",
        "country": "USA",
    },
    {
        "id": "C002",
        "name": "Jane Smith",
        "country": "Canada",
    },
]

# for
licenses = [
    {
        "product": "Microsoft 365",
        "seats": 100,
        "active": True,
        "customer_id": "C001",
    },
    {
        "product": "Windows",
        "seats": 1,
        "active": True,
        "customer_id": "C002",
    },
    {
        "product": "Office",
        "seats": 50,
        "active": False,
        "customer_id": "C001",
    },
    {
        "id": "L004",
        "customer_id": "C999",
        "product": "Azure",
        "seats": 100,
        "active": True,
    },
]


def validate_license(customer, license):
    return (
        license["active"]
        and license["seats"] > 0
        and customer["country"] == "USA"
        and customer["id"] == license["customer_id"]
    )


for license in licenses:
    if validate_license(customer, license):
        print(f"{license['product']} is valid")
    else:
        print(f"{license['product']} is invalid")


def validate_license2(customer, license):
    if not license["active"]:
        return False

    if license["seats"] <= 0:
        return False

    if customer["country"] != "USA":
        return False

    return customer["id"] == license["customer_id"]
