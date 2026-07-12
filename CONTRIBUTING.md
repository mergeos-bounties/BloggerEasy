# Contributing to BloggerEasy

Thank you for your interest in contributing to BloggerEasy — a tool for converting blogs and URLs into clean, well-formatted Markdown or HTML.

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/BloggerEasy.git
   cd BloggerEasy
   ```
3. **Set up a development environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e ".[dev]"
   ```

## Good First Issues

If you're new to the project, look for issues tagged with `good-first-issue` in the [issue tracker](https://github.com/mergeos-bounties/BloggerEasy/issues). These are well-scoped tasks that help you get familiar with the codebase.

## How to Contribute

- **Report bugs** by opening a GitHub Issue.
- **Suggest features** by opening a GitHub Issue with the `enhancement` label.
- **Improve documentation** — corrections, clarifications, and examples are always welcome.
- **Submit code** via a Pull Request.

## Development Workflow

1. Create a feature branch from `master`:
   ```bash
   git checkout -b feat/my-feature
   ```
2. Make your changes.
3. Run linting and tests:
   ```bash
   ruff check src tests
   pytest
   ```
4. Commit with a clear message:
   ```
   feat: add support for WordPress import
   ```
5. Push to your fork and open a Pull Request against `master`.
6. Link any related issues in the PR description using `Closes #N`.

## Code Style

- Follow PEP 8 conventions.
- Run `ruff check` before committing — the CI enforces it.
- Write tests for new functionality.

## Pull Request Checklist

- [ ] Code follows project style (ruff passes)
- [ ] Tests added / updated for new functionality
- [ ] All existing tests pass
- [ ] Documentation updated if needed
- [ ] PR description references related issues

## Need Help?

Open a [Discussion](https://github.com/mergeos-bounties/BloggerEasy/discussions) or ask in the relevant issue.
