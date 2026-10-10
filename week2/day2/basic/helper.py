def determine_approval(invoice_amount):
    if invoice_amount > 1000:
        return "manager Approval Required"
    elif invoice_amount > 500:
        return "supervisor Approval Required"
    else:
        return "standard Approved"

invoice_amount = 750
print(determine_approval(invoice_amount))