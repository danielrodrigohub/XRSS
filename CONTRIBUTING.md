# Contributing to XRSS

First off, thank you for considering contributing to XRSS! It's people like you that make XRSS such a great tool.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:

1. Be respectful and inclusive
2. Exercise consideration and empathy
3. Focus on what is best for the community
4. Give and gracefully accept constructive feedback

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if possible

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* A clear and descriptive title
* A detailed description of the proposed functionality
* Explain why this enhancement would be useful
* List any additional requirements

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the existing style
6. Issue that pull request!

## Development Process

1. Set up your development environment:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install development dependencies
pip install .
```

2. Make your changes:
* Write meaningful commit messages
* Add tests for new functionality
* Update documentation as needed

3. Run the test suite:
```bash
pytest
pytest --cov=xrss tests/  # For coverage report
```

4. Format your code:
```bash
black .
isort .
```

## Style Guide

* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* Use [Black](https://github.com/psf/black) for code formatting
* Add type hints to all functions
* Write docstrings for all public functions
* Keep functions focused and small
* Use meaningful variable names

## Documentation

* Keep README.md up to date
* Document all new features
* Include docstrings in your code
* Update API documentation when needed

## Testing

* Write unit tests for new functionality
* Ensure all tests pass before submitting PR
* Aim for high test coverage
* Include both positive and negative test cases

## Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

## Questions?

Feel free to open an issue with your question or reach out to the maintainers directly.

Thank you for contributing to XRSS! 🎉
