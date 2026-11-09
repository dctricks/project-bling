import sqlite3
import csv

DB = "bling.db"


def setup_database():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def add_sale():
    try:
        amount = float(input("Enter sale amount: $"))

        if not 0 < amount < float("inf"):
            print("Enter a valid positive amount!")
            return

    except ValueError:
        print("Please enter a valid number!")
        return

    with sqlite3.connect(DB) as conn:
        conn.execute(
            "INSERT INTO sales (amount) VALUES (?)",
            (amount,)
        )

    print("Sale saved to database!")


def show_report():
    with sqlite3.connect(DB) as conn:
        result = conn.execute("""
            SELECT COUNT(*), COALESCE(SUM(amount), 0),
                   COALESCE(AVG(amount), 0)
            FROM sales
        """).fetchone()

    count, total, average = result

    print("\n===== PROJECT BLING REPORT =====")
    print("Number of sales:", count)
    print(f"Total revenue: ${total:.2f}")
    print(f"Average sale: ${average:.2f}")


def daily_report():
    sale_date = input("Enter date (YYYY-MM-DD): ")

    with sqlite3.connect(DB) as conn:
        result = conn.execute("""
            SELECT COUNT(*), COALESCE(SUM(amount), 0)
            FROM sales
            WHERE DATE(created_at) = ?
        """, (sale_date,)).fetchone()

    count, total = result

    print("\n===== DAILY SALES REPORT =====")
    print("Date:", sale_date)
    print("Number of sales:", count)
    print(f"Total revenue: ${total:.2f}")


def export_sales():
    with sqlite3.connect(DB) as conn:
        sales = conn.execute(
            "SELECT id, amount, created_at FROM sales ORDER BY id"
        ).fetchall()

    with open("sales_export.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Sale ID", "Amount", "Date"])
        writer.writerows(sales)

    print("Sales exported to sales_export.csv!")
    print("Number of records exported:", len(sales))


def search_sale():
    sale_id = input("Enter sale ID: ")

    with sqlite3.connect(DB) as conn:
        sale = conn.execute(
            "SELECT id, amount, created_at FROM sales WHERE id = ?",
            (sale_id,)
        ).fetchone()

    if sale:
        print("\n===== SALE FOUND =====")
        print("Sale ID:", sale[0])
        print(f"Amount: ${sale[1]:.2f}")
        print("Date:", sale[2])
    else:
        print("Sale not found!")


def show_history():
    with sqlite3.connect(DB) as conn:
        sales = conn.execute(
            "SELECT id, amount, created_at FROM sales ORDER BY id"
        ).fetchall()

    print("\n===== COMPLETE SALES HISTORY =====")

    if not sales:
        print("No sales recorded yet.")
        return

    for sale in sales:
        print(
            f"ID: {sale[0]} | "
            f"Amount: ${sale[1]:.2f} | "
            f"Date: {sale[2]}"
        )


def delete_sale():
    try:
        sale_id = int(input("Enter sale ID to delete: "))

        if sale_id <= 0:
            print("Sale ID must be positive.")
            return

    except ValueError:
        print("Please enter a valid whole number!")
        return

    with sqlite3.connect(DB) as conn:
        sale = conn.execute(
            "SELECT id FROM sales WHERE id = ?",
            (sale_id,)
        ).fetchone()

        if not sale:
            print("Sale ID not found.")
            return

        confirm = input(
            f"Are you sure you want to delete sale {sale_id}? (yes/no): "
        )

        if confirm.lower() != "yes":
            print("Deletion cancelled.")
            return

        conn.execute(
            "DELETE FROM sales WHERE id = ?",
            (sale_id,)
        )

    print("Sale deleted successfully!")


def update_sale():
    try:
        sale_id = int(input("Enter sale ID to update: "))

        if sale_id <= 0:
            print("Sale ID must be positive.")
            return

        new_amount = float(input("Enter corrected sale amount: $"))

        if not 0 < new_amount < float("inf"):
            print("Enter a valid positive amount!")
            return

    except ValueError:
        print("Please enter valid numbers!")
        return

    with sqlite3.connect(DB) as conn:
        sale = conn.execute(
            "SELECT id FROM sales WHERE id = ?",
            (sale_id,)
        ).fetchone()

        if not sale:
            print("Sale ID not found.")
            return

        confirm = input("Confirm update? (yes/no): ")

        if confirm.lower() != "yes":
            print("Update cancelled.")
            return

        conn.execute(
            "UPDATE sales SET amount = ? WHERE id = ?",
            (new_amount, sale_id)
        )

    print("Sale updated successfully!")


def main():
    setup_database()

    while True:
        print("\n===== PROJECT BLING DATABASE =====")
        print("1. Add a sale")
        print("2. View sales report")
        print("3. Search for a sale")
        print("4. View sales history")
        print("5. Delete a sale")
        print("6. Update a sale")
        print("7. Daily sales report")
        print("8. Export sales to CSV")
        print("9. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_sale()
        elif choice == "2":
            show_report()
        elif choice == "3":
            search_sale()
        elif choice == "4":
            show_history()
        elif choice == "5":
            delete_sale()
        elif choice == "6":
            update_sale()
        elif choice == "7":
            daily_report()
        elif choice == "8":
            export_sales()
        elif choice == "9":
            print("Database saved. Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
