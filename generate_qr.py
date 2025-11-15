import qrcode
from PIL import Image
import os
import io

# Define the URL and logo filename (assuming bulsu_logo.png is in the same folder)
TEST_URL = "https://bulsumap-jn5ug9fabhwkxkgzsmh692.streamlit.app"
LOGO_FILENAME = "bulsu_logo.png"


def generate_qr_standalone(data_url, logo_filename):
    """
    Generates a QR code and saves it to a file.
    Note: This is a simplified version for local testing, not for Streamlit.
    """
    try:
        # 1. Create QR Code instance (Requires the real qrcode library)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data_url)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        output_filename = "bulsu_map_qr.png"

        # 2. Handle Logo (Simplified path check)
        if os.path.exists(logo_filename):
            try:
                logo = Image.open(logo_filename).convert('RGBA')
                qr_width, _ = qr_img.size
                logo_size = qr_width // 4
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

                pos = ((qr_width - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
                qr_img.paste(logo, pos, mask=logo)
                print(f"QR Code generated with logo and saved as {output_filename}")
            except Exception as e:
                print(f"Warning: Could not embed logo: {e}. Saving QR without logo.")
        else:
            print(f"Warning: Logo file '{logo_filename}' not found. Saving QR without logo.")

        # 3. Save the final image to a file
        qr_img.save(output_filename)

    except Exception as e:
        print(f"Failed to generate QR code: {e}")


if __name__ == "__main__":
    generate_qr_standalone(TEST_URL, LOGO_FILENAME)