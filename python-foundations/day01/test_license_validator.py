from license_validator import Customer
from license_validator import License
from license_validator import validate_license4


def test_valid_license():
    customer = Customer(
        id="C001",
        name="John Doe",
        country="USA",
    )

    license_info = License(
        id="L001",
        customer_id="C001",
        product="Microsoft 365",
        seats=100,
        active=True,
    )

    assert validate_license4(customer, license_info) is True
    
def test_invalid_license_inactive():
    customer = Customer(
        id="C001",
        name="John Doe",
        country="USA",
    )

    license_info = License(
        id="L002",
        customer_id="C001",
        product="Office",
        seats=50,
        active=False,
    )

    assert validate_license4(customer, license_info) is False
    
def test_invalid_license_seats():
    customer = Customer(
        id="C001",
        name="John Doe",
        country="USA",
    )

    license_info = License(
        id="L003",
        customer_id="C001",
        product="Windows",
        seats=0,
        active=True,
    )

    assert validate_license4(customer, license_info) is False
    
def test_invalid_license_customer_id():
    customer = Customer(
        id="C001",
        name="John Doe",
        country="USA",
    )

    license_info = License(
        id="L004",
        customer_id="C999",
        product="Azure",
        seats=100,
        active=True,
    )

    assert validate_license4(customer, license_info) is False