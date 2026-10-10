invoice_amount = 50000

# 1) if / elif version
if invoice_amount > 50000:
        print("Manager and Director")
elif invoice_amount > 25000:
        print("Manager")
elif invoice_amount < 1000:
        print("Supervisor")
else:
    print("Manager")

# 2) match / case version
match invoice_amount:
        case amt if amt > 50000:
            print("Manager and Director")
        case amt if amt > 25000:
            print("Manager")
        case amt if amt < 1000:
            print("Supervisor")
        case _:
            print("Manager")
# ---------------------------------------------------------------------------
# 3) Employees - print names where len(name) > 6 and salary < 250000
# ---------------------------------------------------------------------------
employees = [
    {"id": 1, "name": "Anil", "salary": 120000},
    {"id": 2, "name": "Sankar", "salary": 260000},
    {"id": 3, "name": "Satish", "salary": 180000},
    {"id": 4, "name": "Prabhakar", "salary": 95000},
    {"id": 5, "name": "Padma", "salary": 240000},
]

print("\nEmployees with name length > 6 and salary < 250000:")
for emp in employees:
    if len(emp["name"]) > 6 and emp["salary"] < 250000:
        print(emp["name"])            