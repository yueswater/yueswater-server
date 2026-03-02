# Yue's Water Blog Backend

This is the core backend engine for [Yue's Water](https://www.yueswater.com/), built on [Python Django](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/). It supports article management, Markdown rendering, reactions, comments, sharing, image uploads, and JWT-based authentication.

## Tech Stack

- **Django 5.x** and **Django REST Framework (DRF)** as the primary backend framework.
- **SimpleJWT** for user authentication and token refresh lifecycle management.
- **Cloudinary** for cloud-based image storage, used for article images and cover photos.
- **Poetry** for dependency management and virtual environment setup.
- **Framer Motion** on the frontend for smooth rendering transitions.
- **Unfold** for a modern Django Admin interface.

## Project Structure

The project follows a modular architecture, separating concerns into distinct Django applications.

- `apps/posts`: Core logic for articles, categories, and tags, with Markdown content storage support.
- `apps/users`: User account management, avatar uploads, and email verification.
- `apps/interactions`: Handles article reactions, comments, shares, and bookmarks.
- `apps/newsletter`: Manages subscription emails and welcome messages.
- `config`: Global settings, including REST Framework configuration, logging, SMTP mail server, and Unfold interface setup.
- `utils`: Custom exception handling, image processing utilities, and a profanity filter.
- `docs`: Database schema design documents in DBML format.

## Core Features

### Image Upload Service and Persistence

The backend exposes a `/api/upload/` endpoint to handle image upload requests. To align with frontend rendering requirements, uploaded images are serialized as HTML tags with specific attributes before being persisted to the database. These attributes include auto-generated unique identifiers such as `id="fig-xxxx"`, ensuring that cross-references and figure numbering remain consistent when content is migrated across platforms.

### Authentication and Token Lifecycle Management

The backend implements a dual-token JWT mechanism. Access token renewal is handled through the `/api/auth/refresh/` endpoint. When the frontend detects a 401 response, the backend validates the provided Refresh Token and issues a new Access Token, ensuring continuity of auto-save operations during long-form editing sessions. A **profanity filter** is also integrated at the data write layer to enforce content compliance at the source.

### Incremental Updates and Auto-Save Support

To support the frontend's automatic snapshot feature, the article endpoints expose the `PATCH` method, allowing partial updates by transmitting only modified fields. This significantly reduces server load from high-frequency requests occurring every 30 seconds and ensures stable synchronization of editor state to the database.

## Environment Configuration

Refer to `.env.example` and configure the following environment variables before starting the project.

- `SECRET_KEY`: Django secret key.
- `CLOUDINARY_URL`: Cloudinary service connection string.
- `CORS_ALLOWED_ORIGINS`: Permitted request origins, e.g. `http://localhost:3000`.
- `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD`: SMTP credentials for sending verification emails.

## Getting Started

Install dependencies and start the development server using Poetry.

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver 8088
```