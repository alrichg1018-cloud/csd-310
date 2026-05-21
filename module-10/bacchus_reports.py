import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "College67!",
    "database": "bacchus_winery",
}


REPORTS = {
    "Supplier Delivery Performance": """
        SELECT 
            supplier.supplier_name,
            supply_delivery.expected_delivery_date,
            supply_delivery.actual_delivery_date,
            DATEDIFF(
                supply_delivery.actual_delivery_date,
                supply_delivery.expected_delivery_date
            ) AS days_late
        FROM supplier
        JOIN supply_delivery
        ON supplier.supplier_id = supply_delivery.supplier_id;
    """,

    "Wine Sales by Distributor": """
        SELECT 
            distributor.distributor_name,
            wine.wine_name,
            wine_order_item.quantity_ordered
        FROM wine_order_item
        JOIN wine
        ON wine_order_item.wine_id = wine.wine_id
        JOIN wine_order
        ON wine_order_item.wine_order_id = wine_order.wine_order_id
        JOIN distributor
        ON wine_order.distributor_id = distributor.distributor_id;
    """,

    "Employee Quarterly Hours": """
        SELECT 
            employee.first_name,
            employee.last_name,
            employee_quarter_hours.work_year,
            employee_quarter_hours.quarter_number,
            employee_quarter_hours.hours_worked
        FROM employee_quarter_hours
        JOIN employee
        ON employee_quarter_hours.employee_id = employee.employee_id;
    """
}


def display_report(cursor, title, query):
    print("\n" + "=" * 80)
    print(title.upper())
    print("=" * 80)

    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    print(" | ".join(columns))
    print("-" * 80)

    for row in rows:
        print(" | ".join(str(value) for value in row))


def main():
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        print("Bacchus Winery Reports")

        for title, query in REPORTS.items():
            display_report(cursor, title, query)

    except Error as err:
        print(f"MySQL Error: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()

        if 'db' in locals() and db.is_connected():
            db.close()
            print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()