from flask import Flask, render_template, request, flash, send_file
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
import base64
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def home():
    img_str = None
    img_filename = None
    if request.method == 'POST':
        data = request.form.get('data')

        if not data:
            flash('Please enter the url for the QR code.')
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

            basewidth = 100
            wpercent = (basewidth / float(logo.size[0]))
            hsize = int((float(logo.size[1]) * float(wpercent)))
            logo = logo.resize((basewidth, hsize), Image.LANCZOS)

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )

            qr.add_data(data)
            qr.make(fit=True)

            # Set custom colors for the QR code
            fill_color = "#143e53"
            back_color = "white"

            img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

            # Ensure QR code image can handle transparency
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, (0, 0), img)
                img = background

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

if __name__ == '__main__':
    app.run(debug=True)
