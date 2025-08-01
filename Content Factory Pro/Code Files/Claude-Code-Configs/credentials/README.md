# Credentials Setup

This directory contains credential files and configuration examples for the Claude Code integrations.

## Files

### `.env.example`
Template for environment variables. Copy this file to `.env` and fill in your actual API keys and configuration values.

### `service-account-key.example.json`
Template for Google Service Account credentials. Replace with your actual service account key file from Google Cloud Console.

## Setup Instructions

1. **Copy the example files:**
   ```bash
   cp .env.example .env
   cp service-account-key.example.json service-account-key.json
   ```

2. **Fill in your credentials:**
   - Edit `.env` with your actual API keys and IDs
   - Replace `service-account-key.json` with your Google Service Account key

3. **Security Notes:**
   - Never commit actual credential files to version control
   - Add `.env` and `service-account-key.json` to your `.gitignore`
   - Keep credentials secure and rotate them regularly

## Required API Keys

- **Notion API Key**: Get from https://www.notion.so/my-integrations
- **Google Drive Service Account**: Create in Google Cloud Console
- **Anthropic API Key**: Get from https://console.anthropic.com/
- **N8N Webhook URL**: From your N8N instance (if applicable)