from dataclasses import dataclass

# Python is dynamically typed
customer_name = "John Doe"
product_name = "Microsoft Office 365"
seats = 100
is_active = True

print(f"Customer Name: {customer_name}")
print(f"Product Name: {product_name}")
print(f"Seats: {seats}")
print(f"Is Active: {is_active}")

# dict, 可以非常自然地混合类型
customer = {
    "id" : "C001",
    "name" : customer_name,
    "country" : "USA",
}

print(customer)
print(f"Customer ID: {customer['id']}")
print(f"Customer Name: {customer['name']}")
print(f"Customer Country: {customer['country']}")
# {'id': 'C001', 'name': 'John Doe', 'country': 'USA'}
# Customer ID: C001
# Customer Name: John Doe

# list, can be list[dict]
customers = [
    {
        "id" : "C001",
        "name" : "John Doe",
        "country" : "USA",
    },
    {
        "id" : "C002",
        "name" : "Jane Smith",
        "country" : "Canada",
    }
]
print(customers)
print(customers[0])
print(customers[1]["name"])

# [{'id': 'C001', 'name': 'John Doe', 'country': 'USA'}, {'id': 'C002', 'name': 'Jane Smith', 'country': 'Canada'}]
# {'id': 'C001', 'name': 'John Doe', 'country': 'USA'}
# Jane Smith

# if
license = {
    "product" : "Microsoft Office 365",
    "seats" : 100,
    "active" : True,
}

if license["active"] and license["seats"] > 0:
    print("License is valid")
else:
    print("License is invalid")
    
# function
def validate_license(license):
    if license["active"] and license["seats"] > 0:
        return True
    return False

result = validate_license(license)
print("function result: ", result)

# for
licenses = [
    {
        "product": "Microsoft 365",
        "seats": 100,
        "active": True,
    },
    {
        "product": "Windows",
        "seats": 0,
        "active": True,
    },
    {
        "product": "Office",
        "seats": 50,
        "active": False,
    },
]
for license in licenses:
    if validate_license(license):
        print(f"{license['product']} is valid")
    else:
        print(f"{license['product']} is invalid")
        
def validate_license2(customer, license):
    if license["active"] and license["seats"] > 0 and customer["country"] == "USA":
        return True
    return False

for license in licenses:
    if validate_license2(customer, license):
        print(f"{license['product']} is valid")
    else:
        print(f"{license['product']} is invalid")
        
class Customer:
    def __init__(self, id: str, name: str, country: str):
        self.id = id
        self.name = name
        self.country = country
        
new_customer = Customer("C002", "Jane Smith", "Canada")
print(new_customer.id)
print(new_customer.name)
print(new_customer.country)

class License:
    def __init__(self, id: str, customer_id: str, product: str, seats: int, active: bool):
        self.id = id
        self.customer_id = customer_id
        self.product = product
        self.seats = seats
        self.active = active
        
license = License(
    "L001",
    "C001",
    "Microsoft 365",
    100,
    True,
)

print(license.product)
print(license.seats)

def validate_license3(customer: Customer, license: License):
    if license.active and license.seats > 0 and customer.country == "USA" and customer.id == license.customer_id:
        return True
    return False


@dataclass
class License:
    id: str
    customer_id: str
    product: str
    seats: int
    active: bool
    
@dataclass
class Customer:
    id: str
    name: str
    country: str
    
def validate_license4(customer: Customer, license: License) -> bool:
    if not license.active:
        return False
    if license.seats <= 0:
        return False
    if customer.country != "USA":
        return False
    if customer.id != license.customer_id:
        return False
    return True

customer = Customer(
    id="C001",
    name="John Doe",
    country="USA",
)

valid_license = License(
    id="L001",
    customer_id="C001",
    product="Microsoft 365",
    seats=100,
    active=True,
)

invalid_license = License(
    id="L002",
    customer_id="C001",
    product="Windows",
    seats=0,
    active=True,
)

print(validate_license4(customer, valid_license))
print(validate_license4(customer, invalid_license))
        