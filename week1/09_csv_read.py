import csv

with open('data/demo_invoices_4.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        try:
            print(row['amount'])
            print(type(row['amount']))
            float_amount = float(row['amount'])
            print(float_amount)
        except ValueError:
            print(f"Invalid amount value: {row['amount']}")