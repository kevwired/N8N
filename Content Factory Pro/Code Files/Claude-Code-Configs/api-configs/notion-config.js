module.exports = {
  // Notion API configuration
  apiVersion: '2022-06-28',
  baseUrl: 'https://api.notion.com/v1',
  headers: {
    'Authorization': `Bearer ${process.env.NOTION_API_KEY}`,
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
  },
  
  // Default database and page settings
  defaultDatabase: process.env.NOTION_DATABASE_ID,
  pageSize: 100,
  
  // Retry configuration
  retryAttempts: 3,
  retryDelay: 1000
};