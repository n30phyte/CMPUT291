import sqlite3

if __name__ == "__main__":
    connection = sqlite3.connect("quiz2.db")
    cursor = connection.cursor()

    color = input("Please input a color: ").strip()

    statement = ("SELECT drivername, driver.age, driver.gender FROM car "
                 "JOIN drives ON drives.carID = car.carID "
                 "JOIN driver ON drives.drivername = driver.name "
                 "WHERE car.color = ? "
                 "ORDER BY driver.age")

    cursor.execute(statement, (color,))
    results = cursor.fetchall()

    if len(results) != 0:
        for res in results:
            print("Name: " + res[0] + ", Age: " + str(res[1]) + ", Gender: " + res[2])
    else:
        print("No results found")
