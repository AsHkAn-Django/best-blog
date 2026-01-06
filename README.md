<p align="center">
<img src="static/images/blog.png" alt="App Screenshot" width="300" height="auto" >
</p>

# Django Blogging System (Full Stack + GraphQL + Real-Time)

[![CI/CD Pipeline](https://github.com/AsHkAn-Django/best-blog/actions/workflows/deploy.yml/badge.svg)](https://github.com/AsHkAn-Django/best-blog/actions/workflows/deploy.yml)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Django](https://img.shields.io/badge/django-5.1-green.svg)
![GraphQL](https://img.shields.io/badge/graphql-graphene-pink.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

A robust, enterprise-grade blogging platform that demonstrates advanced Django patterns. It features a dual-API architecture (REST + GraphQL), real-time notifications via WebSockets, a markdown editor with media support, and a fully Dockerized deployment pipeline.

---

## Key Features

### Core Functionality
- **Dual API Architecture:** Full support for both **REST API** (DRF) and **GraphQL** (Graphene).
- **Real-Time Notifications:** Uses **Django Channels & Redis** to notify users of new replies instantly via WebSockets.
- **Rich Content Editing:** Integrated **SimpleMDE** markdown editor with drag-and-drop image/video support.
- **Social Interaction:** Nested comment threads, upvote/downvote system, and sentiment analysis on user feedback.
- **Smart Recommendations:** dynamically suggests related posts based on tag similarity.

### Technical Highlights
- **Auth:** Secure **JWT (JSON Web Token)** authentication for APIs and Session auth for the web.
- **Background Tasks:** **Celery & Redis** handle heavy tasks like email notifications and media cleanup.
- **Media Management:** Automatic file cleanup (deletes old images when models are updated/deleted) via `django-cleanup`.
- **Infrastructure:** Fully containerized with Docker Compose (Django + Postgres + Redis + Celery).

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Django 5.1, Python 3.11 |
| **APIs** | Django Rest Framework (REST), Graphene (GraphQL) |
| **Real-Time** | Django Channels, Daphne |
| **Database** | PostgreSQL 15 |
| **Caching/Queue** | Redis |
| **Async Tasks** | Celery |
| **Frontend** | Bootstrap 5, SimpleMDE (Markdown) |
| **DevOps** | Docker, GitHub Actions, Nginx |

---

## Installation & Setup (Docker)

The easiest way to run the project is using Docker.

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/blogging-platform.git](https://github.com/yourusername/blogging-platform.git)
    cd blogging-platform
    ```

2.  **Create a `.env` file**
    ```ini
    SECRET_KEY=your_secret_key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1

    # Database
    DB_NAME=blog_db
    DB_USER=blog_user
    DB_PASSWORD=secret
    DB_HOST=db

    # Redis
    REDIS_HOST=redis
    ```

3.  **Build and Run**
    ```bash
    docker compose up -d --build
    ```

4.  **Run Migrations**
    ```bash
    docker compose exec web python manage.py migrate
    ```

The app will be available at: `http://localhost:8004`

---

## API Documentation

### 1. GraphQL API
The project exposes a GraphiQL interface for testing queries.
* **Endpoint:** `/graphql/`

**Example Query:**
```graphql
{
  allPosts {
    title
    author { username }
    comments {
      comment
      author { username }
    }
  }
}
```

**Example Mutation:**

```graphql
mutation {
  createComment(postId: 1, comment: "GraphQL is awesome!") {
    commentObj {
      comment
      author { username }
    }
  }
}
```

2. REST API (JWT Auth)
Secure endpoints using JSON Web Tokens.

 - Get Token: POST /api/token/

    - Body: { "username": "...", "password": "..." }

- Refresh Token: POST /api/token/refresh/

Testing with Tools (Postman/ModHeader): Add the header: Authorization: Bearer ```<your_access_token>```

## Markdown Integration Details
We use SimpleMDE to provide a rich writing experience.

- Field Integration: Models use SimpleMDEField instead of standard TextField.

- Admin Support: The editor is fully integrated into the Django Admin via formfield_overrides.

- Configuration: Global settings control autosave behavior and toolbar options in settings.py.

```Python

# Example: Global Editor Settings
SIMPLEMDE_OPTIONS = {
    'placeholder': 'Start writing in Markdown…',
    'status': False,
    'autosave': {
        'enabled': True,
        'delay': 1000,
    },
}
```

## Testing
The project uses pytest for high-performance testing.
```Bash

# Run all tests inside the container
docker compose exec web pytest
```

## Contact & Portfolio
Ashkan Ahrari - Backend & Deployment Specialist

Portfolio: [codewithashkan.com](https://codewithashkan.com/)

GitHub: [AsHkAn-Django](https://github.com/AsHkAn-Django)

LinkedIn: [Ashkan Ahrari](https://www.linkedin.com/in/ashkan-ahrari/)


I specialize in deploying scalable Django architectures. Open for contract and full-time backend roles.