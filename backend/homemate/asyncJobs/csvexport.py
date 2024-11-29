import csv
from homemate import app
from datetime import datetime
import os
        
def export_to_csv(query_results):
    data = [row.as_dict() for row in query_results]
    if data:
        fieldnames = data[0].keys()
    else:
        print("No data to export.")
        return False,None
    filename = "ServiceRequest_"+datetime.now().strftime('%d-%m-%Y-%H:%M:%S')+".csv"
    path  = os.path.join(app.root_path,"ServiceRequestCSV",filename)
    with open(path, mode="w", newline="", encoding="utf-8") as _file:
        writer = csv.DictWriter(_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return True,filename