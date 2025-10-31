# Quick Start Guide

This guide will help you get started with the Hygraph CMS Translations Manager.

## Prerequisites

Before you begin, make sure you have:
- Python 3.8 or higher installed
- A Hygraph CMS account with two environments (dev and master/production)
- API tokens with appropriate permissions

## Step 1: Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Krugou/hygraphcmspython.git
cd hygraphcmspython
pip install -r requirements.txt
```

## Step 2: Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your Hygraph credentials:

```env
HYGRAPH_DEV_ENDPOINT=https://your-region.hygraph.com/v2/your-dev-project-id/master
HYGRAPH_MASTER_ENDPOINT=https://your-region.hygraph.com/v2/your-master-project-id/master
HYGRAPH_DEV_TOKEN=your_dev_api_token
HYGRAPH_MASTER_TOKEN=your_master_api_token
```

### How to get your API credentials:

1. **API Endpoints:**
   - Go to your Hygraph project
   - Click on "Settings" → "Environments"
   - Copy the Content API endpoint for each environment

2. **API Tokens:**
   - Go to "Settings" → "API Access"
   - Click "Create Token" (or use an existing one)
   - For **Dev environment**: Read permissions are sufficient
   - For **Master environment**: Read, Create, Update, and Publish permissions are required
   - Copy the token and paste it in your `.env` file

## Step 3: Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Step 4: Using the Application

### Initialize Connections

1. Click the "🔌 Initialize Connections" button in the sidebar
2. Wait for the success message confirming both environments are connected
3. Green checkmarks should appear for both Dev and Master environments

### Fetch Translations from Dev

1. Click the "📥 Fetch Dev Translations" button in the Development Environment section
2. The application will load all translations from your dev environment
3. You'll see a list of translations with their keys, values, and locales

### Select Translations to Copy

1. Scroll down to the "📋 Copy Translations from Dev to Master" section
2. Either:
   - Check individual translations you want to copy
   - Or use "Select All Translations" to select everything
3. The counter will show how many translations are selected

### Copy to Master

1. Click the "🚀 Copy X Translation(s) to Master" button
2. Wait for the operation to complete
3. You'll see a success message showing how many translations were copied
4. If any errors occur, they will be displayed with details

### Verify in Master

1. Click "📥 Fetch Master Translations" to refresh the master environment view
2. Verify that your translations now appear in the master environment

## Common Use Cases

### Copying All Translations

This is useful when you want to sync everything from dev to master:

1. Initialize connections
2. Fetch dev translations
3. Click "Select All Translations"
4. Click "Copy to Master"
5. Verify in master

### Copying Specific Translations

When you only want to copy certain translations:

1. Initialize connections
2. Fetch dev translations
3. Review the translations list
4. Select only the ones you need
5. Click "Copy to Master"
6. Verify in master

### Comparing Environments

To see what's different between dev and master:

1. Initialize connections
2. Fetch translations from both environments
3. Compare the lists side-by-side in the two columns
4. Identify which translations are missing in master

## Troubleshooting

### "Missing environment variables" error

- Make sure you've created the `.env` file
- Check that all four variables are set
- Verify there are no typos in variable names

### "Error initializing clients" error

- Verify your API endpoints are correct
- Make sure your tokens are valid and not expired
- Check that you have network access to Hygraph

### "Error fetching translations" error

- Ensure your content model is named "Translation" (case-sensitive)
- Verify the model has the required fields: key, value, locale
- Check that your API token has read permissions

### "Error creating translation" error

- Verify your master token has create permissions
- Check that the translation doesn't already exist
- Ensure all required fields are provided

### Translations not appearing after copy

- Wait a moment and click "Fetch Master Translations" again
- Check if there were any errors during the copy operation
- Verify that the publish operation succeeded

## Tips for Best Practices

1. **Test First**: Always test with a few translations before copying everything
2. **Backup**: Consider backing up your master environment before large operations
3. **Review**: Check the translations in dev before copying to ensure quality
4. **Permissions**: Use tokens with minimal required permissions for security
5. **Environment Variables**: Never commit your `.env` file to version control

## Next Steps

- Customize the GraphQL queries in `hygraph_client.py` for your specific schema
- Add more content models beyond translations
- Extend the UI with additional features like filtering or searching

## Getting Help

If you encounter issues:
- Check the error messages in the UI
- Review the console logs in your terminal
- Refer to the main README.md for more details
- Check Hygraph documentation: https://hygraph.com/docs
- Open an issue on GitHub
