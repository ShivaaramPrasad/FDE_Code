invoices = ["invoice1", "invoice2", "invoice3"]

invoices1 = [{"customer": "John Doe", "amount": 50000, "status": "pending"},
             {"customer": "Jane Smith", "amount": 75000, "status": "approved"},
             {"customer": "Bob Johnson", "amount": 25000, "status": "rejected"}]

invoices1[0]["customer"]="Anil Kumar"
invoices1.append({"customer": "Alice Brown", "amount": 100000, "status": "approved"})
for invoice in invoices1:
    print(f"Customer: {invoice['customer']}, Amount: {invoice['amount']}, Status: {invoice['status']}")