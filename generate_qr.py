import qrcode
from PIL import Image
import os

# Define the URL of the Streamlit app
url = "https://bulsumap-twhdea9bacsvy6jajyfxpk.streamlit.app"  # Replace with your local IP

# Create a QR code instance
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=5,
)
qr.add_data(url)
qr.make(fit=True)

# Generate an image from the QR code instance
qr_img = qr.make_image(fill="black", back_color="white").convert("RGB")

# Path to the logo
logo_path = r"C:\Users\chris\OneDrive\Desktop\bulsu_map\bulsu_logo.png"

# Debugging: Check if logo file exists
if not os.path.exists(logo_path):
    raise FileNotFoundError(f"Logo file not found at {logo_path}")

# Load the logo
logo = Image.open(logo_path)

# Ensure the logo has an alpha channel
if logo.mode != "RGBA":
    logo = logo.convert("RGBA")

# Resize the logo to fit better within the QR code
qr_size = qr_img.size[0]  # Assuming the QR code is square
logo_size = qr_size // 10  # Adjust the size as necessary (1/6 of QR code size)
logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

# Create a mask from the logo's alpha channel
logo_mask = logo.split()[3]  # Extract the alpha channel

# Calculate the position to overlay the logo (centered)
pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)

# Overlay the logo on the QR code using the mask
qr_img.paste(logo, pos, mask=logo_mask)

# Save the QR code with the logo
output_file = "bulsu_map_qr_with_logo_fixed.png"
qr_img.save(output_file)

print(f"✅ QR code with logo generated and saved as {output_file}")
