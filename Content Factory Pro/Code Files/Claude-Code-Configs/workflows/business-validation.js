const anthropicConfig = require('../api-configs/anthropic-config');
const notionHelpers = require('../utils/notion-helpers');
const validation = require('../utils/validation');

class BusinessValidationWorkflow {
  constructor() {
    this.anthropic = anthropicConfig;
    this.validationCriteria = {
      marketFit: ['target_audience', 'problem_statement', 'solution_fit'],
      feasibility: ['technical_requirements', 'resource_needs', 'timeline'],
      viability: ['revenue_model', 'cost_structure', 'competitive_advantage']
    };
  }

  async validateBusinessIdea(ideaData) {
    try {
      const validationResults = {};
      
      for (const [category, criteria] of Object.entries(this.validationCriteria)) {
        validationResults[category] = await this.validateCategory(ideaData, category, criteria);
      }

      const overallScore = this.calculateOverallScore(validationResults);
      const recommendations = await this.generateRecommendations(ideaData, validationResults);

      return {
        idea: ideaData.title || 'Untitled Idea',
        validation_results: validationResults,
        overall_score: overallScore,
        recommendations: recommendations,
        validated_at: new Date().toISOString()
      };
    } catch (error) {
      console.error('Business validation failed:', error);
      throw error;
    }
  }

  async validateCategory(ideaData, category, criteria) {
    const prompt = this.buildValidationPrompt(ideaData, category, criteria);
    
    const response = await this.callAnthropicAPI({
      model: this.anthropic.defaultModel,
      max_tokens: 1000,
      temperature: 0.3,
      messages: [
        {
          role: 'user',
          content: prompt
        }
      ]
    });

    return this.parseValidationResponse(response.content[0].text);
  }

  buildValidationPrompt(ideaData, category, criteria) {
    return `
      Analyze the following business idea for ${category}:
      
      Business Idea: ${ideaData.description || ideaData.title}
      Additional Context: ${JSON.stringify(ideaData, null, 2)}
      
      Evaluate based on these criteria: ${criteria.join(', ')}
      
      Provide a score from 1-10 for each criterion and overall category.
      Include specific feedback and suggestions for improvement.
      
      Format your response as JSON with the following structure:
      {
        "category_score": number,
        "criteria_scores": {
          "criterion_name": {
            "score": number,
            "feedback": "string",
            "suggestions": ["array of suggestions"]
          }
        },
        "summary": "overall category summary"
      }
    `;
  }

  parseValidationResponse(responseText) {
    try {
      return JSON.parse(responseText);
    } catch (error) {
      console.error('Failed to parse validation response:', error);
      return {
        category_score: 5,
        criteria_scores: {},
        summary: 'Unable to parse validation results',
        error: responseText
      };
    }
  }

  calculateOverallScore(validationResults) {
    const categoryScores = Object.values(validationResults)
      .map(result => result.category_score || 0);
    
    return categoryScores.length > 0 
      ? Math.round(categoryScores.reduce((sum, score) => sum + score, 0) / categoryScores.length)
      : 0;
  }

  async generateRecommendations(ideaData, validationResults) {
    const prompt = `
      Based on the following business validation results, provide 3-5 actionable recommendations:
      
      Business Idea: ${ideaData.title || 'Untitled'}
      Validation Results: ${JSON.stringify(validationResults, null, 2)}
      
      Focus on the lowest-scoring areas and provide concrete next steps.
    `;

    const response = await this.callAnthropicAPI({
      model: this.anthropic.defaultModel,
      max_tokens: 800,
      temperature: 0.5,
      messages: [{ role: 'user', content: prompt }]
    });

    return response.content[0].text;
  }

  async saveValidationToNotion(validationResult, databaseId) {
    return await notionHelpers.createPage(databaseId, {
      title: `Validation: ${validationResult.idea}`,
      overall_score: validationResult.overall_score,
      validation_results: JSON.stringify(validationResult.validation_results),
      recommendations: validationResult.recommendations,
      status: 'Validated',
      validated_at: validationResult.validated_at
    });
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

module.exports = BusinessValidationWorkflow;