# Custom QR Code Generator with Flask

This project is a web application built using Flask that generates QR codes with a custom logo and allows users to download the generated QR codes. The QR code color is set to a specific color (`#143e53`).

## Note
### This part of the code in `app.py` was commented while pushing to production

```
# The code below is commented to push to production deployment.
# if __name__ == '__main__':
#     app.run(debug=True)
```
### Uncomment the last two lines if you want to run the project in a development server.
 
## Features

- Generate QR codes with embedded custom logos.
- Custom QR code color.
- Download generated QR codes with one click.

## Prerequisites

- Python 3.x
- Pip (Python package installer)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/cj445/qr-code-generator.git
    cd qr-code-generator
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

- Place your custom logo image in the project directory and name it `logo.png`.

## Running the Application

1. **Run the Flask application:**

    ```bash
    python app.py
    ```

2. **Open your web browser and go to:**

    ```
    http://127.0.0.1:5000
    ```

3. **Generate QR Code:**
    - Enter the data you want to encode into the QR code.
    - Click "Generate QR Code".
    - Your custom QR code will be displayed along with a download button.

## Project Structure

qr-code-generator/

│

├── app.py

├── requirements.txt

├── logo.png

├── static

└── templates/
    └── home.html


## Dependencies

- Flask
- qrcode
- Pillow

## Requirements File

Ensure you have the following in your `requirements.txt`:

Flask==2.1.1
qrcode==7.3.1
Pillow==9.2.0
