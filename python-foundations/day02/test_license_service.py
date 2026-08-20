import pytest
from license_service import Customer, License, validate_license


@pytest.fixture
def customer():
    return Customer(
        id="C001",
        name="John Doe",
        country="USA",
    )


def test_valid_license(customer):
    license_info = License(
        id="L001",
        customer_id="C001",
        product="Microsoft 365",
        seats=100,
        active=True,
    )

    assert validate_license(customer, license_info)


@pytest.mark.parametrize(
    "seats, active, customer_id",
    [
        pytest.param(0, True, "C001", id="zero_seats"),
        pytest.param(50, False, "C001", id="inactive_license"),
        pytest.param(100, True, "C999", id="different_customer"),
    ],
)
def test_invalid_license(customer, seats, active, customer_id):
    license_info = License(
        id="L002",
        customer_id=customer_id,
        product="Office",
        seats=seats,
        active=active,
    )

    assert not validate_license(customer, license_info)


def test_non_usa_customer():
    customer = Customer(
        id="C002",
        name="Jane Smith",
        country="Canada",
    )

    license_info = License(
        id="L004",
        customer_id="C002",
        product="Azure",
        seats=100,
        active=True,
    )

    assert not validate_license(customer, license_info)
