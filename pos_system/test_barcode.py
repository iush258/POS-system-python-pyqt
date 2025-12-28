from utils.barcode_scanner import scan_barcode_live
print("starting scanner")
barcode=scan_barcode_live()

if barcode:
    print("scanned barcode",barcode)
else:
    print("no barcode Detected")