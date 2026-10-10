"""
Classroom Activities (corrected)
Task 1: Invoice approver using if/elif/else and match-case
Task 2: Employees with name length > 6 and salary < 250000
"""

# ---------------------------------------------------------------------------
# TASK 1: INVOICE APPROVER
# Rules: < 1000 -> Supervisor | > 25000 -> Manager | > 50000 -> Manager and Director
# The spec does not cover 1000-25000; assumed Supervisor.
# ---------------------------------------------------------------------------

def approver_if(amount):
    if amount > 50000:
        return "Manager and Director"
    elif amount > 25000:
        return "Manager"
    else:  # < 1000 and the undefined 1000-25000 band
        return "Supervisor"


def approver_match(amount):
    match amount:
        case a if a > 50000:
            return "Manager and Director"
        case a if a > 25000:
            return "Manager"
        case _:
            return "Supervisor"


invoice_amount = 50000
print("TASK 1: INVOICE APPROVER")
print(f"if/elif   : {invoice_amount} -> {approver_if(invoice_amount)}")
print(f"match-case: {invoice_amount} -> {approver_match(invoice_amount)}")

print("\nTesting several amounts:")
for amt in [500, 5000, 25000, 25001, 50000, 50001, 75000]:
    print(f"{amt:>6} -> {approver_if(amt):<22} {approver_match(amt)}")


# ---------------------------------------------------------------------------
# TASK 2: EMPLOYEE FILTER
# ---------------------------------------------------------------------------

employees = [
    (101, "Alice", 45000),
    (102, "Bob", 55000),
    (103, "Christopher", 275000),
    (104, "Diana", 120000),
    (105, "Edward", 89000),
    (106, "Francesca", 195000),
    (107, "Gregory", 310000),
    (108, "Hannah", 155000),
    (109, "Isabella", 220000),
    (110, "Jacob", 75000),
    (111, "Katherine", 240000),
    (112, "Leonardo", 300000),
]

print("\nTASK 2: names with length > 6 and salary < 250000")
for emp_id, name, salary in employees:
    if len(name) > 6 and salary < 250000:
        print(name)
