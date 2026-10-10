file = 'csv'
count =100
if file == 'csv':
    print("File is a CSV file")
elif file == 'json':
    print("File is a JSON file")
elif file == 'xml':
    print("File is an XML file")
else:
    print("File type is not supported")

match file:
    case 'csv':
        print("File is a CSV file")
    case 'json':
        print("File is a JSON file")
    case 'xml':
        print("File is an XML file")
    case _:
        print("File type is not supported")
if (file == 'csv' or file == 'xlsx') and count > 50:
    print("File is a CSV or XLSX file and count is greater than 50")
