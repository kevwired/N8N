module.exports = {
  // Google Drive API configuration
  apiVersion: 'v3',
  baseUrl: 'https://www.googleapis.com/drive/v3',
  
  // Authentication
  scopes: [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
  ],
  
  // Service account configuration
  serviceAccountKeyFile: process.env.GOOGLE_SERVICE_ACCOUNT_KEY_FILE,
  
  // Default folder settings
  defaultFolderId: process.env.GOOGLE_DRIVE_FOLDER_ID,
  
  // Upload configuration
  chunkSize: 262144, // 256KB chunks
  timeout: 30000,
  
  // Retry configuration
  retryAttempts: 3,
  retryDelay: 1000
};