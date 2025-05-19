import qrcode

# Your live Streamlit app URL
url = "https://bulsumap-twhdea9bacsvy6jajyfxpk.streamlit.app"

# Create qr code instance
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=5
)

qr.add_data(url)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill="black", back_color="white")

# Save the image
img.save("bulsu_map_qr.png")

print("✅ QR Code generated and saved as bulsu_map_qr.png!")
