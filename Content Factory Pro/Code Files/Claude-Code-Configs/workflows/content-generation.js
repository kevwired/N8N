const anthropicConfig = require('../api-configs/anthropic-config');
const notionHelpers = require('../utils/notion-helpers');
const driveHelpers = require('../utils/drive-helpers');

class ContentGenerationWorkflow {
  constructor() {
    this.anthropic = anthropicConfig;
  }

  async generateContent(prompt, context = {}) {
    try {
      const response = await this.callAnthropicAPI({
        model: this.anthropic.defaultModel,
        max_tokens: this.anthropic.maxTokens,
        temperature: this.anthropic.temperature,
        messages: [
          {
            role: 'user',
            content: this.buildPrompt(prompt, context)
          }
        ]
      });

      return response.content[0].text;
    } catch (error) {
      console.error('Content generation failed:', error);
      throw error;
    }
  }

  buildPrompt(prompt, context) {
    let fullPrompt = prompt;
    
    if (context.style) {
      fullPrompt += `\n\nStyle guidelines: ${context.style}`;
    }
    
    if (context.audience) {
      fullPrompt += `\n\nTarget audience: ${context.audience}`;
    }
    
    if (context.length) {
      fullPrompt += `\n\nApproximate length: ${context.length}`;
    }

    return fullPrompt;
  }

  async saveToNotion(content, pageTitle, databaseId) {
    return await notionHelpers.createPage(databaseId, {
      title: pageTitle,
      content: content,
      status: 'Generated',
      created_at: new Date().toISOString()
    });
  }

  async saveToGoogleDrive(content, fileName, folderId) {
    return await driveHelpers.uploadTextFile(
      content,
      fileName,
      folderId || process.env.GOOGLE_DRIVE_FOLDER_ID
    );
  }

  async callAnthropicAPI(params) {
    const fetch = require('node-fetch');
    
    const response = await fetch(`${this.anthropic.baseUrl}/v1/messages`, {
      method: 'POST',
      headers: this.anthropic.headers,
      body: JSON.stringify(params)
    });

    if (!response.ok) {
      throw new Error(`Anthropic API error: ${response.statusText}`);
    }

    return await response.json();
  }
}

module.exports = ContentGenerationWorkflow;