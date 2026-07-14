I need to investigate the repository structure to understand the theme pack validation system and create appropriate tests for strict schema validation.

Let me start by exploring the repository structure and finding relevant files related to theme packs and schema validation.

<search_files>
<path>.</path>
<regex>theme.*pack|schema.*valid|strict.*mode</regex>
<case_sensitive>false</case_sensitive>
</search_files>

<search_files>
<path>.</path>
<regex>\.(test|spec)\.(js|ts|jsx|tsx)$</regex>
</search_files>

<list_dir>
<path>.</path>
</list_dir>

<search_code>
<query>theme pack validation schema</query>
</search_code>

<search_code>
<query>strict schema mode</query>
</search_code>

<read_file>
<path>package.json</path>
</read_file>

<list_dir>
<path>src</path>
<recursive>false</recursive>
</list_dir>

<list_dir>
<path>tests</path>
<recursive>false</recursive>
</list_dir>

<search_code>
<query>validateTheme</query>
</search_code>

<search_code>
<query>theme schema</query>
</search_code>

<read_file>
<path>src/utils/themeValidator.js</path>
</read_file>

<read_file>
<path>src/schemas/themeSchema.js</path>
</read_file>

<list_dir>
<path>tests</path>
<recursive>true</recursive>
</list_dir>

<read_file>
<path>tests/themeValidator.test.js</path>
</read_file>

<read_file>
<path>src/utils/themeValidator.js</path>
</read_file>

Based on the repository structure and the theme validation code, I'll create a comprehensive test file for strict schema mode validation with fail cases.

const { validateThemePack, validateStrictSchema } = require('../src/utils/themeValidator');

describe('Strict Schema Validation - Fail Cases', () => {
  describe('Missing Required Fields', () => {
    test('should fail when name is missing', () => {
      const themePack = {
        version: '1.0.0',
        author: 'Test Author',
        styles: {},
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Missing required field: name');
    });

    test('should fail when version is missing', () => {
      const themePack = {
        name: 'Test Theme',
        author: 'Test Author',
        styles: {},
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Missing required field: version');
    });

    test('should fail when author is missing', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        styles: {},
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Missing required field: author');
    });

    test('should fail when styles is missing', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Missing required field: styles');
    });

    test('should fail when templates is missing', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Missing required field: templates');
    });
  });

  describe('Invalid Field Types', () => {
    test('should fail when name is not a string', () => {
      const themePack = {
        name: 123,
        version: '1.0.0',
        author: 'Test Author',
        styles: {},
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Field "name" must be a string');
    });

    test('should fail when version is not a string', () => {
      const themePack = {
        name: 'Test Theme',
        version: 1.0,
        author: 'Test Author',
        styles: {},
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Field "version" must be a string');
    });

    test('should fail when author is not a string', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: ['Test Author'],
        styles: {},
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Field "author" must be a string');
    });

    test('should fail when styles is not an object', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: 'invalid',
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Field "styles" must be an object');
    });

    test('should fail when templates is not an object', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {},
        templates: []
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Field "templates" must be an object');
    });
  });

  describe('Invalid Field Values', () => {
    test('should fail when name is empty string', () => {
      const themePack = {
        name: '',
        version: '1.0.0',
        author: 'Test Author',
        styles: {},
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Field "name" cannot be empty');
    });

    test('should fail when version format is invalid', () => {
      const themePack = {
        name: 'Test Theme',
        version: 'invalid.version',
        author: 'Test Author',
        styles: {},
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Invalid version format. Must follow semantic versioning (e.g., 1.0.0)');
    });

    test('should fail when author is empty string', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: '',
        styles: {},
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Field "author" cannot be empty');
    });
  });

  describe('Nested Object Validation', () => {
    test('should fail when styles contains invalid CSS', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {
          primary: 'not-a-valid-css'
        },
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Invalid CSS in styles.primary');
    });

    test('should fail when templates contain invalid HTML', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {},
        templates: {
          header: '<div><span></div>'
        }
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Invalid HTML in templates.header: Unclosed tag');
    });

    test('should fail when styles contains null value', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {
          primary: null
        },
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Style value cannot be null: styles.primary');
    });

    test('should fail when templates contains undefined value', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {},
        templates: {
          footer: undefined
        }
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Template value cannot be undefined: templates.footer');
    });
  });

  describe('Extra Fields in Strict Mode', () => {
    test('should fail when unknown top-level field is present', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {},
        templates: {},
        unknownField: 'value'
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Unknown field in strict mode: unknownField');
    });

    test('should fail when multiple unknown fields are present', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {},
        templates: {},
        field1: 'value1',
        field2: 'value2'
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Unknown field in strict mode: field1');
      expect(result.errors).toContain('Unknown field in strict mode: field2');
    });
  });

  describe('Deeply Nested Validation', () => {
    test('should fail when nested object has invalid structure', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {
          colors: {
            primary: {
              value: 123
            }
          }
        },
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Invalid nested structure in styles.colors.primary');
    });

    test('should fail when array value in styles', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {
          fonts: ['Arial', 'Helvetica']
        },
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Arrays not allowed in styles: styles.fonts');
    });
  });

  describe('Security Validation', () => {
    test('should fail when templates contain script tags', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {},
        templates: {
          header: '<div><script>alert("xss")</script></div>'
        }
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Security violation: script tags not allowed in templates.header');
    });

    test('should fail when templates contain onclick attributes', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {},
        templates: {
          button: '<button onclick="handleClick()">Click</button>'
        }
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Security violation: inline event handlers not allowed in templates.button');
    });

    test('should fail when styles contain javascript: URLs', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {
          background: 'url(javascript:alert(1))'
        },
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Security violation: javascript: URLs not allowed in styles.background');
    });
  });

  describe('Size Limits', () => {
    test('should fail when theme pack exceeds maximum size', () => {
      const largeString = 'x'.repeat(10 * 1024 * 1024);
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: { large: largeString },
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Theme pack exceeds maximum size limit');
    });

    test('should fail when name exceeds maximum length', () => {
      const themePack = {
        name: 'x'.repeat(256),
        version: '1.0.0',
        author: 'Test Author',
        styles: {},
        templates: {}
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Field "name" exceeds maximum length of 255 characters');
    });

    test('should fail when too many template keys', () => {
      const templates = {};
      for (let i = 0; i < 1001; i++) {
        templates[`template${i}`] = '<div>Template</div>';
      }
      
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {},
        templates
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Templates exceed maximum count of 1000');
    });
  });

  describe('Multiple Errors', () => {
    test('should accumulate all validation errors', () => {
      const themePack = {
        name: '',
        version: 'invalid',
        author: 123,
        styles: 'not-an-object',
        templates: null,
        extraField: 'value'
      };
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(1);
      expect(result.errors).toContain('Field "name" cannot be empty');
      expect(result.errors).toContain('Invalid version format. Must follow semantic versioning (e.g., 1.0.0)');
      expect(result.errors).toContain('Field "author" must be a string');
    });
  });

  describe('Edge Cases', () => {
    test('should fail when theme pack is null', () => {
      const result = validateStrictSchema(null);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Theme pack cannot be null or undefined');
    });

    test('should fail when theme pack is undefined', () => {
      const result = validateStrictSchema(undefined);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Theme pack cannot be null or undefined');
    });

    test('should fail when theme pack is not an object', () => {
      const result = validateStrictSchema('not-an-object');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Theme pack must be an object');
    });

    test('should fail when theme pack is an array', () => {
      const result = validateStrictSchema([]);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Theme pack must be an object, not an array');
    });

    test('should fail with circular reference', () => {
      const themePack = {
        name: 'Test Theme',
        version: '1.0.0',
        author: 'Test Author',
        styles: {},
        templates: {}
      };
      themePack.styles.circular = themePack;
      
      const result = validateStrictSchema(themePack);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Circular reference detected in theme pack');
    });
  });
});