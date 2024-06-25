from flask import Flask, redirect, render_template, request, flash, send_file
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
import base64
import os

# Import styled image classes and modules
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (RoundedModuleDrawer, CircleModuleDrawer, GappedSquareModuleDrawer)
from qrcode.image.styles.colormasks import (RadialGradiantColorMask, SolidFillColorMask)

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def home():
    img_str = None
    img_filename = None
    if request.method == 'POST':
        data = request.form.get('data')
        box_size = request.form.get('box_size', type=int)
        logo_proportion = request.form.get('logo_proportion', type=float)
        style = request.form.get('style')
        color_mask = request.form.get('color_mask')

        if not data:
            flash('Please enter the URL for the QR code.')
            return render_template('home.html')
        if not box_size:
            flash('Please enter the box size for the QR code.')
            return render_template('home.html')
        if not logo_proportion:
            flash('Please enter the logo proportion for the QR code.')
            return render_template('home.html')

        try:
            logo_link = "logo.png"
            if not os.path.exists(logo_link):
                flash('Logo file not found.')
                return render_template('home.html')

            logo = Image.open(logo_link)

            # Ensure logo does not have an alpha channel
            if logo.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', logo.size, (255, 255, 255))
                background.paste(logo, (0, 0), logo)
                logo = background

            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=box_size,
                border=4,
            )

            qr.add_data(data)
            qr.make(fit=True)

            # Select the style
            if style == 'rounded':
                module_drawer = RoundedModuleDrawer()
            elif style == 'circle':
                module_drawer = CircleModuleDrawer()
            elif style == 'gapped':
                module_drawer = GappedSquareModuleDrawer()
            else:
                module_drawer = None  # Default

            # Select the color mask
            if color_mask == 'radial':
                mask = RadialGradiantColorMask()
            elif color_mask == 'solid':
                mask = SolidFillColorMask()
            else:
                mask = None  # Default

            img = qr.make_image(
                fill_color="#143e53",
                back_color="white",
                image_factory=StyledPilImage,
                module_drawer=module_drawer,
                color_mask=mask
            ).convert("RGB")

            # Calculate logo size proportionally to QR code size
            qr_width, qr_height = img.size
            basewidth = int(qr_width * logo_proportion)  # Proportion of QR code size
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.LANCZOS)

            pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
            img.paste(logo, pos)

            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # Save the image temporarily on the server
            img_filename = 'static/qr_code.png'
            img.save(img_filename)

            return render_template('home.html', img_data=img_str, img_filename=img_filename)

        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return render_template('home.html')
    else:
        return render_template('home.html')

@app.route('/download')
def download():
    img_filename = request.args.get('img_filename')
    if img_filename and os.path.exists(img_filename):
        return send_file(img_filename, as_attachment=True, download_name='qr_code.png')
    else:
        flash('File not found.')
        return redirect('/')

# The code below is commented to push to production deployment.
# if __name__ == '__main__':
#     app.run(debug=True)
