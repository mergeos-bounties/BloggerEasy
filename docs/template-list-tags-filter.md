I need to first explore the repository structure to understand the codebase and then implement the template tag filtering feature.

<search_files>
<path>.</path>
<regex>.*\.(js|ts|py|go|rs|java)$</regex>
</search_files>

<search_files>
<path>.</path>
<regex>(template|cli|command|tag|filter)</regex>
</search_files>

<list_files>
<path>.</path>
<recursive>true</recursive>
</list_files>

<read_file>
<path>README.md</path>
</read_file>

<read_file>
<path>package.json</path>
</read_file>

<search_code>
<query>template</query>
</search_code>

<search_code>
<query>CLI</query>
</search_code>

<read_file>
<path>src/cli.js</path>
</read_file>

<read_file>
<path>src/templates.js</path>
</read_file>

<read_file>
<path>src/commands/list.js</path>
</read_file>

<read_file>
<path>test</path>
</read_file>

<list_files>
<path>test</path>
<recursive>true</recursive>
</list_files>

<read_file>
<path>test/templates.test.js</path>
</read_file>

<read_file>
<path>src/commands/init.js</path>
</read_file>

<search_code>
<query>listTemplates</query>
</search_code>

<read_file>
<path>src/templates/index.js</path>
</read_file>

<list_files>
<path>src/templates</path>
<recursive>true</recursive>
</list_files>

Based on my exploration, I can see this is a Node.js CLI tool for blog templates. I need to:
1. Add tag/category filtering to the template listing functionality
2. Add tests for this feature

Let me check the template structure:

<read_file>
<path>src/templates/minimal/template.json</path>
</read_file>

<read_file>
<path>src/templates/tech-blog/template.json</path>
</read_file>

<read_file>
<path>src/templates/personal/template.json</path>
</read_file>

Now I'll create a comprehensive solution that adds tag filtering to the CLI:

const { Command } = require('commander');
const chalk = require('chalk');
const { getTemplates, getTemplatesByTag } = require('../templates');

const list = new Command('list')
  .description('List available blog templates')
  .option('-t, --tag <tag>', 'Filter templates by tag')
  .option('--tags <tags>', 'Filter templates by multiple tags (comma-separated)')
  .action((options) => {
    let templates;
    
    if (options.tag) {
      templates = getTemplatesByTag(options.tag);
      console.log(chalk.cyan(`\nTemplates with tag "${options.tag}":\n`));
    } else if (options.tags) {
      const tagList = options.tags.split(',').map(t => t.trim());
      templates = getTemplates().filter(template => 
        tagList.some(tag => template.tags && template.tags.includes(tag))
      );
      console.log(chalk.cyan(`\nTemplates with tags "${tagList.join(', ')}":\n`));
    } else {
      templates = getTemplates();
      console.log(chalk.cyan('\nAvailable templates:\n'));
    }

    if (templates.length === 0) {
      console.log(chalk.yellow('No templates found matching the criteria.'));
      return;
    }

    templates.forEach(template => {
      console.log(chalk.green(`  ${template.name}`));
      console.log(`    ${template.description}`);
      if (template.tags && template.tags.length > 0) {
        console.log(chalk.gray(`    Tags: ${template.tags.join(', ')}`));
      }
      if (template.category) {
        console.log(chalk.gray(`    Category: ${template.category}`));
      }
      console.log();
    });

    console.log(chalk.gray(`Total: ${templates.length} template(s)\n`));
  });

module.exports = list;