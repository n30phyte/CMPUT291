import sqlite3

if __name__ == "__main__":
    connection = sqlite3.connect("quiz2.db")
    cursor = connection.cursor()

    car_type = input("Please input a car type: ").strip()

    table_name = car_type + "Drives"

    drop = "DROP TABLE IF EXISTS {};".format(table_name)
    create = ("create table {}("
              "drivername char(10),"
              "carID   integer,"
              "PRIMARY KEY (drivername, carID),"
              "FOREIGN KEY (drivername) REFERENCES driver(name),"
              "FOREIGN KEY (carID) REFERENCES car(carID));".format(table_name))

    search = ("SELECT drives.drivername, drives.carID FROM drives "
              "JOIN car ON drives.carID = car.carID "
              "JOIN driver ON drives.drivername = driver.name "
              "WHERE car.type = ?;")

    cursor.execute(drop)
    cursor.execute(create)

    cursor.execute(search, (car_type,))

    headers = cursor.description

    results = cursor.fetchall()

    insert = "INSERT INTO {} VALUES (?, ?)".format(table_name)
    print("{} {}".format(headers[0][0], headers[1][0]))

    for res in results:
        cursor.execute(insert, res)
        print("{} {}".format(res[0], res[1]))

    connection.commit()
