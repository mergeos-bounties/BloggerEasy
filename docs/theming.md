I need to examine the repository structure to understand the project and create an appropriate solution for exporting CSS variable theme tokens.

Let me start by exploring the repository structure:

<search_files>
<path>.</path>
<regex>.*</regex>
</search_files>

<search_files>
<path>.</path>
<regex>\.(css|scss|sass|less|json|js|ts|jsx|tsx)$</regex>
</search_files>

<list_dir>
<path>.</path>
</list_dir>

<read_file>
<path>package.json</path>
</read_file>

<search_code>
<query>theme</query>
<target_type>definition</target_type>
</search_code>

<search_code>
<query>CSS variables</query>
</search_code>

<list_dir>
<path>src</path>
<recursive>true</recursive>
</list_dir>

<read_file>
<path>src/styles/theme.css</path>
</read_file>

<read_file>
<path>src/styles/variables.css</path>
</read_file>

<search_files>
<path>src</path>
<regex>theme|variable|token</regex>
</search_files>

<read_file>
<path>README.md</path>
</read_file>

<list_dir>
<path>src/styles</path>
</list_dir>

<read_file>
<path>src/styles/globals.css</path>
</read_file>

<search_code>
<query>--</query>
<max_results>50</max_results>
</search_code>

Based on my exploration, I'll create a comprehensive solution for exporting CSS variable theme tokens to JSON format. This will include:

1. A script to parse CSS variables and export them as design tokens
2. Documentation on how to use the export functionality

```javascript
const fs = require('fs');
const path = require('path');
const postcss = require('postcss');

/**
 * CSS Theme Tokens Exporter
 * Extracts CSS custom properties (variables) from stylesheets and exports them as JSON design tokens
 */

class ThemeTokensExporter {
  constructor(options = {}) {
    this.cssFiles = options.cssFiles || ['src/styles/globals.css', 'src/styles/theme.css', 'src/styles/variables.css'];
    this.outputPath = options.outputPath || 'theme-tokens.json';
    this.includeComments = options.includeComments !== false;
  }

  /**
   * Parse CSS file and extract custom properties
   */
  async parseCSSFile(filePath) {
    try {
      const cssContent = fs.readFileSync(filePath, 'utf8');
      const result = await postcss().process(cssContent, { from: filePath });
      const tokens = {};

      result.root.walkRules((rule) => {
        const selector = rule.selector;
        let category = 'global';

        // Determine category from selector
        if (selector.includes(':root')) {
          category = 'root';
        } else if (selector.includes('[data-theme="dark"]')) {
          category = 'dark';
        } else if (selector.includes('[data-theme="light"]')) {
          category = 'light';
        } else if (selector.match(/\.([\w-]+)/)) {
          category = selector.match(/\.([\w-]+)/)[1];
        }

        if (!tokens[category]) {
          tokens[category] = {};
        }

        let currentComment = '';
        rule.walkComments((comment) => {
          currentComment = comment.text.trim();
        });

        rule.walkDecls((decl) => {
          if (decl.prop.startsWith('--')) {
            const tokenName = decl.prop.slice(2);
            const tokenValue = decl.value;
            
            const tokenData = {
              value: tokenValue,
              selector: selector
            };

            if (this.includeComments && currentComment) {
              tokenData.description = currentComment;
            }

            // Parse token type based on value
            if (tokenValue.match(/^#[0-9a-fA-F]{3,8}$/) || 
                tokenValue.match(/^rgb|rgba|hsl|hsla/)) {
              tokenData.type = 'color';
            } else if (tokenValue.match(/^\d+(\.\d+)?(px|rem|em|%|vh|vw)$/)) {
              tokenData.type = 'dimension';
            } else if (tokenValue.match(/^\d+(\.\d+)?$/)) {
              tokenData.type = 'number';
            } else if (tokenValue.match(/^(['"])[^'"]*\1$|^[\w\s-]+$/)) {
              tokenData.type = 'font-family';
            } else {
              tokenData.type = 'other';
            }

            tokens[category][tokenName] = tokenData;
          }
        });
      });

      return tokens;
    } catch (error) {
      console.error(`Error parsing ${filePath}:`, error.message);
      return {};
    }
  }

  /**
   * Merge tokens from multiple files
   */
  mergeTokens(tokensArray) {
    const merged = {};

    tokensArray.forEach((tokens) => {
      Object.keys(tokens).forEach((category) => {
        if (!merged[category]) {
          merged[category] = {};
        }
        Object.assign(merged[category], tokens[category]);
      });
    });

    return merged;
  }

  /**
   * Group tokens by semantic categories
   */
  categorizeTokens(tokens) {
    const categorized = {
      colors: {},
      spacing: {},
      typography: {},
      borders: {},
      shadows: {},
      transitions: {},
      breakpoints: {},
      zIndex: {},
      other: {}
    };

    Object.keys(tokens).forEach((themeKey) => {
      Object.keys(tokens[themeKey]).forEach((tokenName) => {
        const token = tokens[themeKey][tokenName];
        let targetCategory = 'other';

        if (tokenName.includes('color') || tokenName.includes('bg') || 
            tokenName.includes('background') || token.type === 'color') {
          targetCategory = 'colors';
        } else if (tokenName.includes('spacing') || tokenName.includes('gap') || 
                   tokenName.includes('margin') || tokenName.includes('padding')) {
          targetCategory = 'spacing';
        } else if (tokenName.includes('font') || tokenName.includes('text') || 
                   tokenName.includes('line-height') || tokenName.includes('letter-spacing')) {
          targetCategory = 'typography';
        } else if (tokenName.includes('border') || tokenName.includes('radius')) {
          targetCategory = 'borders';
        } else if (tokenName.includes('shadow')) {
          targetCategory = 'shadows';
        } else if (tokenName.includes('transition') || tokenName.includes('duration') || 
                   tokenName.includes('ease')) {
          targetCategory = 'transitions';
        } else if (tokenName.includes('breakpoint') || tokenName.includes('screen')) {
          targetCategory = 'breakpoints';
        } else if (tokenName.includes('z-index') || tokenName.includes('layer')) {
          targetCategory = 'zIndex';
        }

        if (!categorized[targetCategory][themeKey]) {
          categorized[targetCategory][themeKey] = {};
        }
        categorized[targetCategory][themeKey][tokenName] = token;
      });
    });

    // Remove empty categories
    Object.keys(categorized).forEach((cat) => {
      if (Object.keys(categorized[cat]).length === 0) {
        delete categorized[cat];
      }
    });

    return categorized;
  }

  /**
   * Export tokens to JSON file
   */
  async export() {
    try {
      console.log('Extracting CSS theme tokens...');
      
      const allTokens = [];
      for (const cssFile of this.cssFiles) {
        const filePath = path.resolve(cssFile);
        if (fs.existsSync(filePath)) {
          console.log(`Parsing ${cssFile}...`);
          const tokens = await this.parseCSSFile(filePath);
          allTokens.push(tokens);
        } else {
          console.warn(`File not found: ${cssFile}`);
        }
      }

      const mergedTokens = this.mergeTokens(allTokens);
      const categorizedTokens = this.categorizeTokens(mergedTokens);

      const output = {
        version: '1.0.0',
        generatedAt: new Date().toISOString(),
        tokens: categorizedTokens,
        raw: mergedTokens
      };

      fs.writeFileSync(this.outputPath, JSON.stringify(output, null, 2));
      console.log(`✅ Theme tokens exported to ${this.outputPath}`);
      
      const tokenCount = Object.values(mergedTokens)
        .reduce((sum, cat) => sum + Object.keys(cat).length, 0);
      console.log(`📊 Extracted ${tokenCount} tokens`);

      return output;
    } catch (error) {
      console.error('Error exporting tokens:', error);
      throw error;
    }
  }

  /**
   * Export to multiple formats
   */
  async exportToFormats(formats = ['json', 'js', 'scss', 'css']) {
    const tokens = await this.export();

    if (formats.includes('js')) {
      const jsContent = `export const themeTokens = ${JSON.stringify(tokens, null, 2)};`;
      fs.writeFileSync(this.outputPath.replace('.json', '.js'), jsContent);
      console.log(`✅ Exported to ${this.outputPath.replace('.json', '.js')}`);
    }

    if (formats.includes('scss')) {
      let scssContent = '// Generated SCSS variables from theme tokens\n\n';
      Object.keys(tokens.raw).forEach((theme) => {
        scssContent += `// ${theme.toUpperCase()} Theme\n`;
        Object.keys(tokens.raw[theme]).forEach((token) => {
          scssContent += `$${token}: ${tokens.raw[theme][token].value};\n`;
        });
        scssContent += '\n';
      });
      fs.writeFileSync(this.outputPath.replace('.json', '.scss'), scssContent);
      console.log(`✅ Exported to ${this.outputPath.replace('.json', '.scss')}`);
    }

    if (formats.includes('css')) {
      let cssContent = '/* Generated CSS variables from theme tokens */\n\n';
      Object.keys(tokens.raw).forEach((theme) => {
        const selector = theme === 'root' ? ':root' : `.theme-${theme}`;
        cssContent += `${selector} {\n`;
        Object.keys(tokens.raw[theme]).forEach((token) => {
          cssContent += `  --${token}: ${tokens.raw[theme][token].value};\n`;
        });
        cssContent += '}\n\n';
      });
      fs.writeFileSync(this.outputPath.replace('.json', '.css'), cssContent);
      console.log(`✅ Exported to ${this.outputPath.replace('.json', '.css')}`);
    }

    return tokens;
  }
}

// CLI Interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {
    cssFiles: args.length > 0 ? args : undefined,
    outputPath: 'theme-tokens.json',
    includeComments: true
  };

  const exporter = new ThemeTokensExporter(options);
  
  exporter.exportToFormats(['json', 'js', 'scss', 'css'])
    .then(() => {
      console.log('\n✨ All exports completed successfully!');
      process.exit(0);
    })
    .catch((error) => {
      console.error('Export failed:', error);
      process.exit(1);
    });
}

module.exports = ThemeTokensExporter;