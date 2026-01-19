# Logistics Analytics Pipeline and Dashboard

## Overview

An end-to-end data analytics solution that simulates a logistics company's operations, analyzing delivery performance, driver efficiency, and shipping trends. This project demonstrates practical skills in database design, ETL development, and business intelligence reporting.

**Key capabilities:**
- Normalized PostgreSQL database with enforced referential integrity
- Python ETL pipeline generating 300,000+ realistic records
- Interactive Power BI dashboard with advanced analytics

## Technology Stack

**Database:** PostgreSQL 16  
**ETL Development:** Python 3.14 (psycopg2, Faker)  
**Business Intelligence:** Power BI Desktop (DAX, Power Query)  
**Design Patterns:** Star schema, role-playing dimensions, batch processing

## Project Structure

- `sql/` — Database schema DDL and analytical queries
- `scripts/` — ETL pipeline for data generation
- `dashboard/` — Power BI analytics dashboard (.pbix)

## Features

### Database Design

Models the complete package lifecycle from creation through final delivery.

**Entity model includes:**
- Customers, Drivers, Vehicles, Packages, Tracking Events
- Foreign key constraints ensuring referential integrity
- Enumerated types for package status (`created`, `out_for_delivery`, `delivered`)

### Python ETL Pipeline

The `seed_logistics.py` script generates operationally realistic data:

- **Realistic profiles:** Leverages Faker library for authentic customer names, addresses, and contact information
- **Logical sequencing:** Enforces business rules (pickup events always follow package creation)
- **Scalable performance:** Batched inserts efficiently handle 300,000+ record datasets

### Power BI Dashboard

![The Dashboard](images/Logistics_Project.pdf)

Direct-query connection to PostgreSQL optimized through star schema architecture.

**Advanced analytics features:**
- **Role-playing dimensions:** Separates Customers table into Senders and Recipients, enabling independent origin/destination analysis
- **Custom DAX measures:** Calculates delivery success rate, actual vs. estimated delivery time variance, and other KPIs
- **Interactive drill-through:** Click-through from driver-level metrics to individual package details

## Business Value

This project demonstrates how data engineering and analytics can answer critical logistics questions: Which routes consistently miss delivery windows? Which drivers maintain the highest success rates? How do shipping volumes fluctuate across regions? The dashboard transforms raw operational data into actionable insights for route optimization, resource allocation, and performance management.