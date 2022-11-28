import json, csv, xmltodict, sqlite3, os
from pycnic.core import WSGI, Handler

koneksi = sqlite3.connect('Cars.db')
cursor = koneksi.cursor()

class Json(Handler):
  def get(self):
    file = open('CarsData/Cars.json')
    data = json.load(file)
    return data

class CSV(Handler):
  def get(self):
    data = []
    with open('CarsData/Cars.csv') as file_data:
        csv_file = csv.reader(file_data)
        for index, row in enumerate(csv_file):
            if int(index) >= 1:
                object = {"Id": row[0], "Name": row[1], "Price": row[2]}
                data.append(object)
    return data

class XML(Handler):
  def get(self):
    with open('CarsData/Cars.xml') as file_data:
      json_data = xmltodict.parse(file_data.read())
    
      row_data = json_data['root']['row']
      row_data.remove(row_data[0])
    return row_data

class ListData(Handler):
  def get(self):
    data = []

    cursor.execute("SELECT * FROM cars_data")
    for row in cursor.fetchall():
      object = {"Id": row[0], "Brand": row[1], "Model": row[2], "Price": row[3]}
      data.append(object)
    koneksi.commit()

    return data

class AddData(Handler):
  def post(self):
    brand = self.request.data["brand"]
    model = self.request.data["model"]
    price = self.request.data["price"]

    value = (brand, model, price)
    cursor.execute("INSERT INTO cars_data (brand,model,price) VALUES(?, ?, ?);", value)
    koneksi.commit()

    return {'message': 'Success'}

class EditData(Handler):
  def post(self):
    id = self.request.data["id"]
    converted = "% s" % id
    
    cursor.execute("SELECT * FROM cars_data WHERE id = '"+converted+"'")
    for row in cursor.fetchall():
      object = {"Id": row[0], "Brand": row[1], "Model": row[2], "Price": row[3]}
    koneksi.commit()

    return object

class UpdateData(Handler):
  def post(self):
    brand = self.request.data["brand"]
    model = self.request.data["model"]
    price = self.request.data["price"]
    id = self.request.data["id"]
    converted = "% s" % id

    cursor.execute("UPDATE cars_data SET brand = '"+brand+"', model = '"+model+"', price = '"+price+"' WHERE id = '"+converted+"'")
    koneksi.commit()

    return {'message': 'Success'}

class DeleteData(Handler):
  def post(self):
    id = self.request.data["id"]
    converted = "% s" % id

    cursor.execute("DELETE FROM cars_data WHERE id = '"+converted+"'")
    koneksi.commit()

    return {'message': 'Success'}

class app(WSGI):
  headers = [("Access-Control-Allow-Origin", "*")]
  routes = [
            ('/', Json()),
            ('/csv', CSV()),
            ('/xml', XML()),
            ('/list', ListData()),
            ('/add', AddData()),
            ('/edit', EditData()),
            ('/update', UpdateData()),
            ('/delete', DeleteData()),
  ]