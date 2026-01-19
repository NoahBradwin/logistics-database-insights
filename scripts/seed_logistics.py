import psycopg2
import random
from faker import Faker
from datetime import datetime, timedelta

DB_HOST = "localhost"
DB_NAME = "Logistics Project"
DB_USER = "*****"
DB_PASS = "*****"

fake = Faker()

conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
cur = conn.cursor()

def create_customers(n=100):
    customer_ids = []
    for _ in range(n):
        name = fake.name()
        email = fake.unique.email()
        phone = fake.phone_number()[:20]
        address = fake.address().replace('\n', ', ')

        cur.execute(
            "INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s) RETURNING id",
            (name, email, phone, address)
        )
        customer_ids.append(cur.fetchone()[0])
    return customer_ids

def create_drivers(n=10):
    driver_ids = []
    for _ in range(n):
        name = fake.name()
        license_num = fake.unique.license_plate()
        phone = fake.phone_number()[:20]
        
        cur.execute(
            "INSERT INTO drivers (name, license_number, phone) VALUES (%s, %s, %s) RETURNING id",
            (name, license_num, phone)
        )
        driver_ids.append(cur.fetchone()[0])
    return driver_ids

def create_packages_and_history(n_packages, customer_ids, driver_ids):
    statuses = ['created', 'picked_up', 'at_warehouse', 'out_for_delivery', 'delivered', 'cancelled']
    
    for _ in range(n_packages):
        sender = random.choice(customer_ids)
        recipient = random.choice(customer_ids)
        while recipient == sender: recipient = random.choice(customer_ids)
        
        driver = random.choice(driver_ids)
        weight = round(random.uniform(0.5, 50.0), 2)
        tracking_num = "TRK-" + fake.unique.bothify(text='??####')
        
        final_status = random.choices(statuses, weights=[5, 10, 20, 15, 45, 5])[0]
        
        delivery_date = fake.date_time_between(start_date='-1y', end_date='now')
        
        cur.execute("""
            INSERT INTO packages (tracking_number, sender_id, recipient_id, weight_kg, assigned_driver_id, current_status, estimated_delivery, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (tracking_num, sender, recipient, weight, driver, final_status, delivery_date.date(), delivery_date - timedelta(days=3)))
        
        pkg_id = cur.fetchone()[0]

        history_time = delivery_date - timedelta(days=3)
        cur.execute("INSERT INTO tracking_events (package_id, status, event_location, event_time) VALUES (%s, %s, %s, %s)",
                    (pkg_id, 'created', 'System Origin', history_time))

        if final_status in ['picked_up', 'at_warehouse', 'out_for_delivery', 'delivered']:
            history_time += timedelta(hours=random.randint(2, 6))
            cur.execute("INSERT INTO tracking_events (package_id, status, event_location, event_time) VALUES (%s, %s, %s, %s)",
                        (pkg_id, 'picked_up', fake.address(), history_time))

        if final_status in ['at_warehouse', 'out_for_delivery', 'delivered']:
            history_time += timedelta(hours=random.randint(4, 12))
            cur.execute("INSERT INTO tracking_events (package_id, status, event_location, event_time) VALUES (%s, %s, %s, %s)",
                        (pkg_id, 'at_warehouse', 'Distribution Center ' + random.choice(['A','B','C']), history_time))

        if final_status == 'delivered':
            cur.execute("INSERT INTO tracking_events (package_id, status, event_location, event_time) VALUES (%s, %s, %s, %s)",
                        (pkg_id, 'delivered', 'Customer Front Door', delivery_date))

def main():
    try:
        cust_ids = create_customers(20000)
        drv_ids = create_drivers(200)
        create_packages_and_history(300000, cust_ids, drv_ids)
        
        conn.commit()
        print("Done")

    except Exception as e:
        print("Error:", e)
        conn.rollback()

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()