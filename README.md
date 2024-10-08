# Text Analysis Django Application

## Overview

This Django application provides text analysis and translation services using AI-driven tools. It allows users to input text, choose an output language, and receive analyzed results.

## Features

1. User Authentication
2. Text Analysis
3. Multi-language Support
4. Recent Analyses Display
5. User Profile Management

## Project Structure

The main application is located in the `django-app/myapp` directory. Key files and directories include:

- `main/`: Contains the core application logic
- `myapp/`: Contains project-wide settings and configurations
- `stylesheets/`: Houses static files including CSS and JavaScript
- `tests/`: Contains test files for the application

## Setup and Installation

1. Ensure you have Python and Django installed.
2. Clone the repository.
3. Install the required dependencies:
   ```
   pip install -r djangorequirements.txt
   ```
4. Set up your environment variables (refer to the `.env` file).
5. Run migrations:
   ```
   python manage.py migrate
   ```
6. Start the development server:
   ```
   python manage.py runserver
   ```

## Key Components

### Models

The main model is `Analysis`, which stores user text inputs and analysis results. You can find the model definition in [django-app/myapp/main/models.py](django-app/myapp/main/models.py).

### Views

Key views include:

- Homepage
- User Login/Logout
- User Registration
- User Profile
- Text Analysis

For details, refer to [django-app/myapp/main/views.py](django-app/myapp/main/views.py).

### Forms

The `TextAnalysisForm` handles user input for text analysis. You can find the form definition in [django-app/myapp/main/forms.py](django-app/myapp/main/forms.py).

### Templates

The application uses a base template (`base.html`) and extends it for specific pages like the homepage and analysis results.

### Static Files

CSS styles are defined in [django-app/myapp/main/static/main.css](django-app/myapp/main/static/main.css).

## Configuration

### Settings

Important settings are located in [django-app/myapp/myapp/settings.py](django-app/myapp/myapp/settings.py).

Key configurations include database settings, installed apps, middleware, and logging.

### URL Configuration

Main URL patterns are defined in `myapp/urls.py`.

## Testing

Tests are written using pytest. The configuration for pytest is in [django-app/myapp/pytest.ini](django-app/myapp/pytest.ini).

To run tests, use the command: