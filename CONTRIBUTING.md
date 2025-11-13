# Contributing to InsightCore

Thank you for your interest in contributing to InsightCore! This document provides guidelines and instructions for contributing to the project.

## 🚧 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Community](#community)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [maintainers].

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** for backend development
- **Node.js 18+** for frontend development
- **Docker** and **Docker Compose**
- **Git**
- **Redis** (for caching and queues)
- **PostgreSQL** with PostGIS extension

### Development Environment Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/insightcore.git
   cd insightcore
   git remote add upstream https://github.com/original-org/insightcore.git
   ```

2. **Create a virtual environment for backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

5. **Run database migrations**
   ```bash
   cd backend
   python manage.py migrate
   python manage.py createsuperuser
   ```

## 🏗️ Project Structure

```
insight-core/
├── backend/                 # Django backend application
│   ├── core/               # Django settings, URLs, middleware
│   ├── cameras/            # Camera-related models and views
│   ├── analytics/          # Analytics models and business logic
│   ├── videos/             # Video processing models
│   ├── events/             # Event models and processing
│   ├── alerts/             # Alert system models
│   ├── api/                # REST API endpoints
│   └── manage.py           # Django management script
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── pages/          # Page-level components
│   │   ├── api/            # API service calls
│   │   ├── hooks/          # Custom React hooks
│   │   └── utils/          # Utility functions
│   ├── public/             # Static assets
│   └── package.json        # Frontend dependencies
├── analyzer/               # Video analysis service
│   ├── analyzer_service.py # Main analysis service
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Container configuration
├── monitoring/             # Monitoring configurations
├── .github/                # GitHub configuration
│   └── workflows/          # CI/CD workflows
├── docker-compose.yml      # Docker orchestration
├── README.md               # Project documentation
└── CONTRIBUTING.md         # This file
```

## 🔄 Development Workflow

### 1. Branch Strategy

- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/**: Feature branches (e.g., `feature/camera-management`)
- **bugfix/**: Bug fix branches (e.g., `bugfix/login-issue`)
- **hotfix/**: Critical production fixes

### 2. Creating a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### 3. Making Changes

- Write clean, well-documented code
- Follow the coding standards below
- Write tests for your changes
- Update documentation as needed

### 4. Commit Messages

Use conventional commits format:

```
<type>(<scope>): <short summary>
<BLANK LINE>
<body - optional>
<BLANK LINE>
<footer - optional>
```

Examples:
- `feat(camera): add RTSP stream validation`
- `fix(analytics): resolve memory leak in object tracking`
- `docs: update API documentation for events`

## 📝 Coding Standards

### Backend (Python/Django)

- **Style**: Follow PEP 8
- **Imports**: Use absolute imports
- **Naming**: Use snake_case for functions/variables, PascalCase for classes
- **Docstrings**: Use Google-style docstrings
- **Type hints**: Use type hints for all functions

```python
def process_video_frame(frame: np.ndarray, camera_id: str) -> List[Detection]:
    """Process a single video frame and detect objects.
    
    Args:
        frame: Input video frame as numpy array
        camera_id: Unique identifier for the camera
        
    Returns:
        List of detected objects with their properties
    """
    # Implementation here
    pass
```

### Frontend (React/TypeScript)

- **Style**: Follow Airbnb JavaScript Style Guide
- **Naming**: Use PascalCase for components, camelCase for functions/variables
- **TypeScript**: Use TypeScript for type safety
- **Components**: Keep components small and focused
- **Hooks**: Use custom hooks for reusable logic

```typescript
interface Camera {
  id: string;
  name: string;
  rtspUrl: string;
  status: 'active' | 'inactive' | 'error';
}

const CameraCard: React.FC<{ camera: Camera }> = ({ camera }) => {
 // Component implementation
 return <div>{camera.name}</div>;
};
```

### Database Models

- Use descriptive field names
- Add `help_text` for complex fields
- Use `choices` for limited options
- Add `verbose_name` and `verbose_name_plural` for clarity

```python
class Event(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='medium',
        help_text="Severity level of the event"
    )
```

## 🧪 Testing

### Backend Tests

Run all tests:
```bash
cd backend
python -m pytest
```

Run tests with coverage:
```bash
python -m pytest --cov=.
```

Add new tests in `backend/tests/` following the structure:
```
backend/tests/
├── test_models.py
├── test_views.py
├── test_api.py
└── conftest.py
```

### Frontend Tests

Run tests:
```bash
cd frontend
npm test
```

Run tests with coverage:
```bash
npm test -- --coverage
```

### Test Standards

- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test API endpoints and database interactions
- **Coverage**: Aim for 80%+ test coverage
- **Naming**: Use descriptive test names

## 📚 Documentation

### Code Documentation

- **Python**: Use Google-style docstrings
- **JavaScript/TypeScript**: Use JSDoc comments
- **API**: Document all endpoints in `docs/api.md`

### Architecture Documentation

Update architecture diagrams and design decisions in:
- `docs/architecture.md`
- `docs/decisions/` (Architecture Decision Records)

### User Documentation

- Update README.md for new features
- Add user guides in `docs/guides/`
- Update API documentation

## 📤 Submitting Changes

### 1. Before Submitting

```bash
# Run all tests
python -m pytest  # Backend
npm test          # Frontend

# Run linters
flake8 backend/   # Python linting
npm run lint      # Frontend linting

# Update documentation
# Make sure README.md and other docs are updated
```

### 2. Commit and Push

```bash
git add .
git commit -m "feat: add camera management functionality"
git push origin feature/your-feature-name
```

### 3. Create Pull Request

- Go to the repository on GitHub
- Click "New pull request"
- Select your feature branch
- Fill in the PR template:
  - **Title**: Clear, concise description
  - **Description**: What was changed and why
  - **Related Issues**: Link to related issues
 - **Testing**: How to test the changes
  - **Checklist**: Confirm all requirements are met

### 4. PR Review Process

- Maintainers will review your code
- Address feedback and make changes
- PR will be merged after approval
- Branch will be deleted after merge

## 🤝 Community

### Getting Help

- **Issues**: Report bugs or request features
- **Discussions**: Ask questions and share ideas
- **Documentation**: Check existing docs first

### Code Review Guidelines

When reviewing code, consider:
- **Functionality**: Does it work as expected?
- **Code Quality**: Is it clean and maintainable?
- **Security**: Are there any security concerns?
- **Performance**: Is it efficient?
- **Tests**: Are there adequate tests?
- **Documentation**: Is it well-documented?

## 🆘 Need Help?

If you have questions about contributing:
- Check the existing documentation
- Open an issue with your question
- Join our community discussions

---

Thank you for contributing to InsightCore! Your efforts help make video analytics more accessible and effective for industrial safety and security.