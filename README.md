# Hygraph CMS Translations Manager 🌐

A Python-based web application for managing and copying content translations between Hygraph CMS environments (dev to master).

## Features

- 🔌 Connect to multiple Hygraph environments (dev and master)
- 📥 Fetch translations from both environments
- 📋 View and compare translations
- ✅ Select individual or all translations to copy
- 🚀 Copy translations from dev to master with one click
- 📊 Visual feedback on copy operations
- 🎨 User-friendly web interface built with Streamlit

## Prerequisites

- Python 3.8 or higher
- Hygraph CMS account with:
  - Dev environment API endpoint and token
  - Master environment API endpoint and token
  - Appropriate permissions (read from dev, write to master)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Krugou/hygraphcmspython.git
cd hygraphcmspython
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` file with your Hygraph credentials:
```env
HYGRAPH_DEV_ENDPOINT=https://your-region.hygraph.com/v2/your-dev-project-id/master
HYGRAPH_MASTER_ENDPOINT=https://your-region.hygraph.com/v2/your-master-project-id/master
HYGRAPH_DEV_TOKEN=your_dev_api_token
HYGRAPH_MASTER_TOKEN=your_master_api_token
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown (typically http://localhost:8501)

3. Follow these steps in the UI:
   - Click "Initialize Connections" in the sidebar
   - Click "Fetch Dev Translations" to load translations from dev
   - Select the translations you want to copy (or use "Select All")
   - Click "Copy X Translation(s) to Master"
   - Verify the results in the Master environment section

## Project Structure

```
hygraphcmspython/
├── app.py                 # Main Streamlit application
├── hygraph_client.py      # Hygraph API client
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
└── README.md             # This file
```

## Configuration

### Hygraph API Tokens

You need to create API tokens in your Hygraph project:

1. Go to your Hygraph project settings
2. Navigate to "API Access"
3. Create a Permanent Auth Token with appropriate permissions:
   - **Dev token**: Read permissions
   - **Master token**: Read and Write permissions (including publish)

### Content Model

This application expects a `Translation` model in your Hygraph schema with the following fields:
- `key` (String): Translation key
- `value` (String): Translation value
- `locale` (String): Locale code (e.g., 'en', 'fi', 'sv')

You can customize the schema by modifying the GraphQL queries in `hygraph_client.py`.

## API Client Methods

The `HygraphClient` class provides the following methods:

- `get_translations()`: Fetch all translations
- `create_translation(key, value, locale)`: Create a new translation
- `publish_translation(translation_id)`: Publish a translation
- `execute_query(query, variables)`: Execute custom GraphQL queries
- `introspect_schema()`: Discover available content models

## Troubleshooting

### Connection Issues
- Verify your API endpoints are correct
- Check that your API tokens have the necessary permissions
- Ensure your network allows connections to Hygraph

### Translation Errors
- Check that the Translation model exists in both environments
- Verify field names match the schema
- Review the error messages in the UI for specific issues

## Security Notes

- Never commit your `.env` file to version control
- Keep your API tokens secure
- Use tokens with minimal required permissions
- Regularly rotate your API tokens

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Open an issue on GitHub
- Check Hygraph documentation: https://hygraph.com/docs

