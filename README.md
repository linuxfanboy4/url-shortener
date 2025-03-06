# Quantum Link - Advanced URL Shortener

Quantum Link is a sophisticated URL shortener built with Flask, SQLAlchemy, and QR code generation capabilities. It provides a seamless experience for creating short URLs, managing custom aliases, and tracking analytics. The application is designed with a modern, responsive UI and advanced features such as QR code generation and detailed click statistics.

## Features

1. **URL Shortening**:
   - Generate short URLs with customizable lengths (6, 8, or 10 characters).
   - Create custom aliases for personalized short URLs.
   - Validate URLs to ensure they start with `http://` or `https://`.

2. **QR Code Generation**:
   - Automatically generate QR codes for shortened URLs.
   - Download QR codes as PNG images.

3. **Analytics Dashboard**:
   - Track the number of clicks for each shortened URL.
   - View creation timestamps for all URLs.
   - Sort URLs by creation date for easy management.

4. **Responsive Design**:
   - Modern, gradient-based UI with a glass-morphism effect.
   - Fully responsive layout for desktop and mobile devices.

5. **Database Integration**:
   - Uses SQLite for persistent storage of URLs and their metadata.
   - Tracks clicks and creation times for advanced analytics.

6. **Copy to Clipboard**:
   - Easily copy shortened URLs to the clipboard with a single click.

## Installation

To set up Quantum Link on your local machine, follow these steps:

1. **Clone the Repository**:
   ```bash
   wget https://raw.githubusercontent.com/linuxfanboy4/url-shortener/refs/heads/main/app.py
   ```

2. **Install Dependencies**:
   Ensure you have Python installed, then install the required dependencies using pip:
   ```bash
   pip install flask flask-sqlalchemy qrcode[pil]
   ```

3. **Run the Application**:
   Execute the following command to start the Flask server:
   ```bash
   python app.py
   ```

4. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:5000` to use Quantum Link.

## Usage

### Creating a Short URL

1. **Enter the Original URL**:
   - Input the full URL you want to shorten in the provided field.

2. **Choose an Option**:
   - **Random**: Generate a random short URL with a specified length (6, 8, or 10 characters).
   - **Custom**: Create a custom alias for your short URL (4-20 characters, letters, numbers, underscores, or hyphens).

3. **Submit**:
   - Click "Create Short URL" to generate the shortened link.

4. **Copy or Share**:
   - Use the "Copy URL" button to copy the shortened link to your clipboard.
   - Download the QR code for easy sharing.

### Viewing Analytics

1. **Access the Dashboard**:
   - Click the "View Advanced Analytics" link on the homepage.

2. **Review Statistics**:
   - View all shortened URLs, their original links, click counts, and creation dates.
   - Sort URLs by creation date for better organization.

## Code Structure

- **Flask Application**:
  - The application is built using Flask, a lightweight web framework for Python.
  - Routes are defined for home, redirection, analytics, and QR code generation.

- **Database**:
  - SQLite is used for storing URL data, including original URLs, short URLs, click counts, and creation timestamps.
  - SQLAlchemy is used as the ORM for database interactions.

- **QR Code Generation**:
  - The `qrcode` library is used to generate QR codes for shortened URLs.
  - QR codes are served as PNG images using Flask's `send_file` function.

- **Templates**:
  - HTML templates are rendered using Flask's `render_template_string` function.
  - The UI is styled with modern CSS, including gradients, glass-morphism effects, and responsive design.

## Contributing

Contributions are welcome! If you'd like to contribute to Quantum Link, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your change

## License

Quantum Link is open-source software licensed under the MIT License. See the LICENSE file for more details.

## Support

For support or feature requests, please open an issue on the GitHub repository.
