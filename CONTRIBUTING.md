# Contributing Guide

Thank you for your interest in contributing to our Flask web application! This guide will help you understand how to contribute effectively.

## Architecture Overview

The application follows a layered architecture:

1. **Database Models**: Define the data structure and relationships
2. **Repositories**: Handle database operations and queries
3. **DTO Objects**: Data Transfer Objects for API responses/requests
4. **Services**: Business logic layer
5. **Generators**: Utility classes for generating content/files
6. **Controllers**: Handle HTTP requests and responses
7. **API Endpoints**: RESTful routes definition
8. **Templates**: Jinja2 HTML templates
9. **Stylesheets**: CSS files for styling
10. **Scripts**: JavaScript files for client-side functionality

## Getting Started

### Prerequisites
- Python 3.8+
- pip
- PostgreSQL (or your preferred database)
- Node.js (for frontend assets if applicable)

### Installation
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables (copy `.env.example` to `.env` and configure)
6. Run database migrations: `flask db upgrade`

## Development Workflow

### Branching Strategy
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Feature branches (prefix with `feature/`)
- `bugfix/*` - Bug fix branches (prefix with `bugfix/`)

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for test related changes
- `chore:` for maintenance tasks

### Pull Requests
1. Create a branch from `develop`
2. Make your changes with clear, atomic commits
3. Push your branch and open a PR against `develop`
4. Ensure all tests pass and code coverage remains high
5. Request review from at least one maintainer

## Coding Standards

### Python Code
- Follow [PEP 8](https://pep8.org/) style guide
- Type hints for all new code
- Docstrings following Google style format
- Keep functions small and focused
- Write unit tests for all new functionality

### Frontend Code
- HTML: Semantic markup in templates
- CSS: Follow BEM methodology
- JavaScript: ES6+ syntax, minimal DOM manipulation

### Testing
- Unit tests for all business logic
- Integration tests for API endpoints
- End-to-end tests for critical user flows
- Aim for 80%+ test coverage

## How new service should look like:

```
├── feature/                   
    ├── controllers/          # Route controllers
    ├── dto/                  # Data Transfer Objects
    ├── models/               # Database models
    ├── repositories/         # Database operations
    ├── services/             # Business logic
    ├── generators/           # Content generators
    ├── static/               # Static files
    │   ├── css/              # Stylesheets
    │   ├── js/               # Scripts
    ├── templates/            # Jinja2 templates
    ├── __init__.py           # Application factory
    ├── tests/                # Test suite
    └── README.md             # Feature documentation        
```

## Reporting Issues
- Check existing issues before creating new ones
- Provide clear steps to reproduce
- Include error messages and screenshots if applicable
- Specify environment details

## Feature Requests
- Explain the problem you're trying to solve
- Describe your proposed solution
- Provide examples if applicable

## Code Review Process
1. PR is opened and CI pipeline runs
2. Maintainers review within 2 business days
3. Address any feedback by pushing new commits
4. PR is merged after approval and passing checks

Thank you for contributing!
