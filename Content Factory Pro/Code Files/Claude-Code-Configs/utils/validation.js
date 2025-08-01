class ValidationHelpers {
  constructor() {
    this.rules = {};
  }

  // Email validation
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  // URL validation
  isValidUrl(url) {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  }

  // Phone number validation (basic international format)
  isValidPhone(phone) {
    const phoneRegex = /^\+?[\d\s\-\(\)]{10,}$/;
    return phoneRegex.test(phone);
  }

  // Required field validation
  isRequired(value) {
    return value !== null && value !== undefined && value !== '';
  }

  // String length validation
  isValidLength(value, minLength = 0, maxLength = Infinity) {
    if (typeof value !== 'string') return false;
    return value.length >= minLength && value.length <= maxLength;
  }

  // Number range validation
  isInRange(value, min = -Infinity, max = Infinity) {
    const num = Number(value);
    if (isNaN(num)) return false;
    return num >= min && num <= max;
  }

  // Date validation
  isValidDate(dateString) {
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
  }

  // Future date validation
  isFutureDate(dateString) {
    if (!this.isValidDate(dateString)) return false;
    const date = new Date(dateString);
    return date > new Date();
  }

  // Past date validation
  isPastDate(dateString) {
    if (!this.isValidDate(dateString)) return false;
    const date = new Date(dateString);
    return date < new Date();
  }

  // API key validation (basic format check)
  isValidApiKey(apiKey, expectedLength = null) {
    if (!apiKey || typeof apiKey !== 'string') return false;
    if (expectedLength && apiKey.length !== expectedLength) return false;
    return /^[a-zA-Z0-9_-]+$/.test(apiKey);
  }

  // JSON validation
  isValidJson(jsonString) {
    try {
      JSON.parse(jsonString);
      return true;
    } catch {
      return false;
    }
  }

  // Business idea validation
  validateBusinessIdea(idea) {
    const errors = [];
    const warnings = [];

    // Required fields
    if (!this.isRequired(idea.title)) {
      errors.push('Business idea title is required');
    }

    if (!this.isRequired(idea.description)) {
      errors.push('Business idea description is required');
    }

    // Length validations
    if (idea.title && !this.isValidLength(idea.title, 5, 100)) {
      errors.push('Title must be between 5 and 100 characters');
    }

    if (idea.description && !this.isValidLength(idea.description, 20, 1000)) {
      errors.push('Description must be between 20 and 1000 characters');
    }

    // Optional field validations
    if (idea.target_audience && !this.isValidLength(idea.target_audience, 5, 200)) {
      warnings.push('Target audience description should be between 5 and 200 characters');
    }

    if (idea.estimated_revenue && !this.isInRange(idea.estimated_revenue, 0)) {
      errors.push('Estimated revenue must be a positive number');
    }

    if (idea.timeline && !this.isValidLength(idea.timeline, 5, 100)) {
      warnings.push('Timeline should be between 5 and 100 characters');
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  }

  // Content validation
  validateContent(content) {
    const errors = [];
    const warnings = [];

    if (!this.isRequired(content.title)) {
      errors.push('Content title is required');
    }

    if (!this.isRequired(content.body)) {
      errors.push('Content body is required');
    }

    if (content.title && !this.isValidLength(content.title, 5, 200)) {
      errors.push('Title must be between 5 and 200 characters');
    }

    if (content.body && !this.isValidLength(content.body, 50)) {
      warnings.push('Content body seems short (less than 50 characters)');
    }

    if (content.tags && Array.isArray(content.tags)) {
      content.tags.forEach((tag, index) => {
        if (!this.isValidLength(tag, 2, 30)) {
          warnings.push(`Tag ${index + 1} should be between 2 and 30 characters`);
        }
      });
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  }

  // API configuration validation
  validateApiConfig(config, requiredFields = []) {
    const errors = [];
    const warnings = [];

    // Check required fields
    requiredFields.forEach(field => {
      if (!this.isRequired(config[field])) {
        errors.push(`${field} is required`);
      }
    });

    // Validate API keys
    if (config.apiKey && !this.isValidApiKey(config.apiKey)) {
      errors.push('API key format is invalid');
    }

    if (config.anthropicApiKey && !this.isValidApiKey(config.anthropicApiKey)) {
      errors.push('Anthropic API key format is invalid');
    }

    // Validate URLs
    if (config.baseUrl && !this.isValidUrl(config.baseUrl)) {
      errors.push('Base URL is invalid');
    }

    if (config.webhookUrl && !this.isValidUrl(config.webhookUrl)) {
      errors.push('Webhook URL is invalid');
    }

    // Validate numeric values
    if (config.timeout && !this.isInRange(config.timeout, 1000, 300000)) {
      warnings.push('Timeout should be between 1000ms and 300000ms');
    }

    if (config.retryAttempts && !this.isInRange(config.retryAttempts, 1, 10)) {
      warnings.push('Retry attempts should be between 1 and 10');
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  }

  // File validation
  validateFile(file, allowedExtensions = [], maxSizeBytes = null) {
    const errors = [];
    const warnings = [];

    if (!file || !file.name) {
      errors.push('File name is required');
      return { isValid: false, errors, warnings };
    }

    // Check file extension
    if (allowedExtensions.length > 0) {
      const extension = file.name.split('.').pop().toLowerCase();
      if (!allowedExtensions.includes(`.${extension}`)) {
        errors.push(`File type .${extension} is not allowed. Allowed types: ${allowedExtensions.join(', ')}`);
      }
    }

    // Check file size
    if (maxSizeBytes && file.size > maxSizeBytes) {
      errors.push(`File size (${file.size} bytes) exceeds maximum allowed size (${maxSizeBytes} bytes)`);
    }

    // Warnings for large files
    if (file.size > 10 * 1024 * 1024) { // 10MB
      warnings.push('Large file detected - upload may take longer');
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  }

  // Custom validation rule
  addRule(name, validatorFunction) {
    this.rules[name] = validatorFunction;
  }

  // Apply custom rule
  applyRule(ruleName, value, ...args) {
    if (!this.rules[ruleName]) {
      throw new Error(`Validation rule '${ruleName}' not found`);
    }
    return this.rules[ruleName](value, ...args);
  }

  // Bulk validation
  validateBulk(data, validationSchema) {
    const results = {};
    
    for (const [field, rules] of Object.entries(validationSchema)) {
      const fieldValue = data[field];
      const fieldErrors = [];
      const fieldWarnings = [];

      rules.forEach(rule => {
        const { type, params = [], required = false } = rule;
        
        // Skip validation if field is empty and not required
        if (!required && !this.isRequired(fieldValue)) {
          return;
        }

        // Apply validation based on type
        let isValid = false;
        switch (type) {
          case 'required':
            isValid = this.isRequired(fieldValue);
            break;
          case 'email':
            isValid = this.isValidEmail(fieldValue);
            break;
          case 'url':
            isValid = this.isValidUrl(fieldValue);
            break;
          case 'length':
            isValid = this.isValidLength(fieldValue, ...params);
            break;
          case 'range':
            isValid = this.isInRange(fieldValue, ...params);
            break;
          case 'custom':
            isValid = this.applyRule(params[0], fieldValue, ...params.slice(1));
            break;
          default:
            fieldWarnings.push(`Unknown validation type: ${type}`);
        }

        if (!isValid) {
          fieldErrors.push(rule.message || `${field} validation failed for rule: ${type}`);
        }
      });

      results[field] = {
        isValid: fieldErrors.length === 0,
        errors: fieldErrors,
        warnings: fieldWarnings
      };
    }

    return {
      isValid: Object.values(results).every(result => result.isValid),
      results
    };
  }
}

module.exports = new ValidationHelpers();