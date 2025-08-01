const notionConfig = require('../api-configs/notion-config');

class NotionHelpers {
  constructor() {
    this.config = notionConfig;
  }

  async createPage(databaseId, properties) {
    try {
      const response = await this.makeRequest('/pages', 'POST', {
        parent: { database_id: databaseId },
        properties: this.formatProperties(properties)
      });
      
      return response;
    } catch (error) {
      console.error('Failed to create Notion page:', error);
      throw error;
    }
  }

  async updatePage(pageId, properties) {
    try {
      const response = await this.makeRequest(`/pages/${pageId}`, 'PATCH', {
        properties: this.formatProperties(properties)
      });
      
      return response;
    } catch (error) {
      console.error('Failed to update Notion page:', error);
      throw error;
    }
  }

  async queryDatabase(databaseId, filter = {}, sorts = []) {
    try {
      const response = await this.makeRequest(`/databases/${databaseId}/query`, 'POST', {
        filter,
        sorts,
        page_size: this.config.pageSize
      });
      
      return response.results;
    } catch (error) {
      console.error('Failed to query Notion database:', error);
      throw error;
    }
  }

  async getPage(pageId) {
    try {
      const response = await this.makeRequest(`/pages/${pageId}`, 'GET');
      return response;
    } catch (error) {
      console.error('Failed to get Notion page:', error);
      throw error;
    }
  }

  async getDatabase(databaseId) {
    try {
      const response = await this.makeRequest(`/databases/${databaseId}`, 'GET');
      return response;
    } catch (error) {
      console.error('Failed to get Notion database:', error);
      throw error;
    }
  }

  async appendBlocksToPage(pageId, blocks) {
    try {
      const response = await this.makeRequest(`/blocks/${pageId}/children`, 'PATCH', {
        children: blocks
      });
      
      return response;
    } catch (error) {
      console.error('Failed to append blocks to Notion page:', error);
      throw error;
    }
  }

  formatProperties(properties) {
    const formatted = {};
    
    for (const [key, value] of Object.entries(properties)) {
      if (typeof value === 'string') {
        formatted[key] = {
          type: 'rich_text',
          rich_text: [{ type: 'text', text: { content: value } }]
        };
      } else if (typeof value === 'number') {
        formatted[key] = {
          type: 'number',
          number: value
        };
      } else if (typeof value === 'boolean') {
        formatted[key] = {
          type: 'checkbox',
          checkbox: value
        };
      } else if (value instanceof Date) {
        formatted[key] = {
          type: 'date',
          date: { start: value.toISOString().split('T')[0] }
        };
      } else if (Array.isArray(value)) {
        formatted[key] = {
          type: 'multi_select',
          multi_select: value.map(item => ({ name: item }))
        };
      } else if (key === 'title') {
        formatted[key] = {
          type: 'title',
          title: [{ type: 'text', text: { content: value } }]
        };
      }
    }
    
    return formatted;
  }

  createTextBlock(content) {
    return {
      type: 'paragraph',
      paragraph: {
        rich_text: [{ type: 'text', text: { content } }]
      }
    };
  }

  createHeadingBlock(content, level = 1) {
    const headingType = `heading_${level}`;
    return {
      type: headingType,
      [headingType]: {
        rich_text: [{ type: 'text', text: { content } }]
      }
    };
  }

  createListBlock(items, ordered = false) {
    const listType = ordered ? 'numbered_list_item' : 'bulleted_list_item';
    
    return items.map(item => ({
      type: listType,
      [listType]: {
        rich_text: [{ type: 'text', text: { content: item } }]
      }
    }));
  }

  async makeRequest(endpoint, method = 'GET', body = null) {
    const fetch = require('node-fetch');
    
    const options = {
      method,
      headers: this.config.headers
    };
    
    if (body) {
      options.body = JSON.stringify(body);
    }
    
    let retries = 0;
    while (retries < this.config.retryAttempts) {
      try {
        const response = await fetch(`${this.config.baseUrl}${endpoint}`, options);
        
        if (!response.ok) {
          throw new Error(`Notion API error: ${response.status} ${response.statusText}`);
        }
        
        return await response.json();
      } catch (error) {
        retries++;
        if (retries >= this.config.retryAttempts) {
          throw error;
        }
        
        await new Promise(resolve => setTimeout(resolve, this.config.retryDelay * retries));
      }
    }
  }
}

module.exports = new NotionHelpers();