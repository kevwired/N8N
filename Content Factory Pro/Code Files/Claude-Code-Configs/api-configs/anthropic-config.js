module.exports = {
  // Anthropic Claude API configuration
  apiVersion: '2023-06-01',
  baseUrl: 'https://api.anthropic.com',
  
  // Authentication
  apiKey: process.env.ANTHROPIC_API_KEY,
  
  // Model configuration
  defaultModel: 'claude-3-sonnet-20240229',
  maxTokens: 4096,
  temperature: 0.7,
  
  // Headers
  headers: {
    'Content-Type': 'application/json',
    'x-api-key': process.env.ANTHROPIC_API_KEY,
    'anthropic-version': '2023-06-01'
  },
  
  // Retry configuration
  retryAttempts: 3,
  retryDelay: 1000,
  timeout: 60000
};