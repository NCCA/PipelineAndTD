#!/usr/bin/env -S uv run --script
import sqlite3
import sys

DB_PATH = "TheComputerStore.db"


def main(db_path=DB_PATH):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        print("Demo based on Computer Store code")
        print("***************************************")
        print("Select all products")
        print("---------------------------------------")
        for row in cur.execute("SELECT * FROM Products;"):
            # Expecting: Code, Name, Price, Manufacturer
            code, name, price, manufacturer = row
            print(code, name, price, manufacturer)

        print("***************************************")
        print("Select the names of all the products in the store")
        print("---------------------------------------")
        for (name,) in cur.execute("SELECT Name FROM Products;"):
            print(name)

        print("***************************************")
        print("Select the name of the products with a price less than or equal to $200.")
        print("---------------------------------------")
        for (name,) in cur.execute("SELECT Name FROM Products WHERE Price <= 200;"):
            print(name)

        print("***************************************")
        print("Select all the products with a price between $60 and $120.")
        print("---------------------------------------")
        for row in cur.execute("SELECT * FROM Products WHERE Price BETWEEN 60 AND 120;"):
            code, name, price, manufacturer = row
            print(code, name, price, manufacturer)

        print("***************************************")
        print("average price")
        print("---------------------------------------")
        cur.execute("SELECT AVG(Price) FROM Products WHERE Manufacturer=2;")
        avg_row = cur.fetchone()
        avg_price = avg_row[0] if avg_row and avg_row[0] is not None else None
        if avg_price is not None:
            print(f"Average price ${avg_price}")
        else:
            print("Average price: <no results>")

        print("***************************************")
        print("Select the names of manufacturer whose products have an average price larger than or equal to $150.")
        print("---------------------------------------")
        query = """
            SELECT AVG(Price) AS avg_price, Manufacturers.Name
            FROM Products
            INNER JOIN Manufacturers
              ON Products.Manufacturer = Manufacturers.Code
            GROUP BY Manufacturers.Name
            HAVING AVG(Price) >= 150;
        """
        for avg_price, name in cur.execute(query):
            # Print name then average price to match the C++ demo output order
            print(name, avg_price)

    except sqlite3.Error as e:
        print("SQLite error:", e, file=sys.stderr)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
    finally:
        try:
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
