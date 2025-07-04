# EZ-Backend

# Secure File-Sharing System

A modern, secure file-sharing system built with FastAPI and React, supporting two user types: **Ops Users** (who can upload files) and **Client Users** (who can sign up, verify email, and download files via secure links).

---

## Features

- **Ops User:**
  - Login
  - Upload files (pptx, docx, xlsx only)
- **Client User:**
  - Sign up (email verification required)
  - Login
  - List all uploaded files
  - Request secure, one-time download links
  - Download files (link is user-specific and expires)
- **Security:**
  - JWT authentication
  - Password hashing (bcrypt)
  - Role-based access
  - File type validation
  - Email verification
  - CORS enabled for frontend-backend communication

---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite (dev) / PostgreSQL (prod)
- **Frontend:** React (Vite), Material-UI
- **Auth:** JWT (python-jose)
- **Testing:** Pytest, FastAPI TestClient
- **Containerization:** Docker

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo>
```

### 2. Backend Setup
```bash
cd backend  # or project root if not separated
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Environment Variables
- Set your DB URL, JWT secret, etc. in environment variables or a `.env` file.

### 5. Run the Backend
```bash
uvicorn app.main:app --reload
```

### 6. Run the Frontend
```bash
cd frontend
npm run dev
```

---

## API Usage (Main Endpoints)

### **Ops User**
- `POST /ops/login` — Login as Ops
- `POST /ops/upload-file` — Upload file (pptx, docx, xlsx only)

### **Client User**
- `POST /client/signup` — Sign up (returns verification URL)
- `GET /client/verify-email?token=...` — Verify email
- `POST /client/login` — Login
- `GET /client/files` — List all files
- `POST /client/download-file/{file_id}` — Get secure download link
- `GET /client/download/{token}` — Download file

---

## Testing

- **Run all tests:**
  ```bash
  pytest
  ```
- Tests use pytest fixtures to create an Ops user and cover all major flows (login, upload, signup, verify, download).

---

## Deployment

1. **Containerize with Docker:**
   - See provided `Dockerfile`.
2. **Use a production database:**
   - PostgreSQL or MySQL (set DB URL in env vars).
3. **Set environment variables:**
   - For secrets, DB URL, etc.
4. **Use a reverse proxy:**
   - Nginx or Caddy for HTTPS and static files.
5. **Deploy to cloud:**
   - AWS, Azure, GCP, DigitalOcean, Render, Heroku, etc.
6. **Set up CI/CD:**
   - Use GitHub Actions or similar for automated testing and deployment.

---

## Security Best Practices
- Use HTTPS in production
- Set strong secrets in environment variables
- Regularly update dependencies
- Monitor logs and errors
- Restrict CORS to your frontend domain

---

## License

MIT License
