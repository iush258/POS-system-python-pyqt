
# POS-system-python-pyqt-mongodb

## 🛒 POS System with Python, MongoDB & Barcode Scanner

* A simple Point of Sale (POS) system built in Python with the following features:
* GUI using PyQt
* MongoDB for storing product, sales, and user data
* Barcode scanning using a camera (via OpenCV + pyzbar)
* Product management (add, update, delete, view)
* Sales processing with cart & billing
* Reports for sales summary

# 🔦 Features
## 📦 Product Management

* Add new products with details (name, price, stock, barcode).
* Edit or delete existing products.
* Auto-add new products when scanned for the first time.

## 🎥 Barcode Scanning

* Uses camera as scanner to fetch product info.
* If product is not found, user can add details and save to DB.

## 🛍️ POS Terminal

* Add items to cart by scanning or selecting.
* Generates total bill.
* Updates stock after each sale.

## 📊 Reports & Analytics

+ Daily/weekly/monthly sales reports.
+ View inventory levels.

## 🛠️ Tech Stack
+ Python 3.10+
+ PyQt5 / PySide6 → GUI
+ MongoDB → Database
+ OpenCV → Camera handling
+ pyzbar → Barcode/QR code detection

## ✅ Future Enhancements
+ Add receipt printing (PDF/thermal printer).
+ Implement user roles (cashier, admin).
+ Add discounts and offers feature.
+ Cloud sync support.

# ⚡ Getting Started
## 1️⃣ Clone the Repo
`git clone https://github.com/your-username/pos-system.git`
`cd pos-system`

## 2️⃣ Install Dependencies
`pip install -r requirements.txt`

## 3️⃣ Run MongoDB
+ Make sure MongoDB is running on your system:

`mongod`

## 4️⃣ Start the App
`python main.py`


# 📁File Structure
```
pos_system/
│── config/
│   ├── db.py           # MongoDB connection setup
│
│── models/
│   ├── products.py     # Product model & DB functions
│   ├── sales.py        # Sales model & functions
│   ├── users.py        # (Optional) user management
│
│── ui/
│   ├── main_window.py  # Main GUI window
│   ├── product_ui.py   # Product management GUI
│   ├── sales_ui.py     # Sales/checkout GUI
│
│── utils/
│   ├── barcode_scanner.py  # Barcode scanning using camera
│
│── main.py             # Entry point of the app
```
# Dependencies
copy this txt into notepad and save it as requirements.txt

```
# Core Dependencies
pyqt5==5.15.9        # For GUI (or you can use PySide6 if preferred)
pymongo==4.5.0       # For MongoDB connection
opencv-python==4.8.0.74  # For camera handling
pyzbar==0.1.9        # For barcode/QR code scanning

# Utility
numpy==1.25.0        # Required by OpenCV
```

## ⚡ Install all dependencies
` pip install -r requirements.txt  `
