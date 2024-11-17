# FastAPI Auth API

🚀 **FastAPI Auth API** adalah sebuah aplikasi authentication yang dibangun menggunakan FastAPI. Project ini mendukung login berbasis token JWT dengan hashing password menggunakan `bcrypt`. 

## Features

- 🔒 **Authentication**: Login dengan username dan password.
- 🔐 **JWT Token**: Menggunakan `HS256` untuk keamanan.
- 📦 **Modular Code**: Struktur code rapi dengan model, auth, dan konfigurasi terpisah.
- 🌐 **CORS Support**: Dibuka untuk domain tertentu (disesuaikan di `origins`).

---

## Installation

Ikuti langkah-langkah di bawah ini untuk menjalankan project ini di lokal:

### 1. Clone Repo
```bash
git clone https://github.com/cpamungkas/fastapi_auth_sample.git
cd fastapi_auth_sample
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Running Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Server akan berjalan di: http://localhost:8000

## API Endpoints
### Auth
<table><thead><tr><th>Method</th><th>Endpoint</th><th>Description</th></tr></thead><tbody><tr><td><code>POST</code></td><td><code>/token</code></td><td>Generate JWT token</td></tr><tr><td><code>GET</code></td><td><code>/users/me</code></td><td>Get current logged-in user</td></tr></tbody></table>

### Example Request Login
```bash
POST /token
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=secret
```

### Example Response Login
```bash
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
  "token_type": "bearer"
}
```

## Project Structure
```bash
repo-name/
├── app/
│   ├── __init__.py
│   ├── auth.py        # Authentication logic
│   ├── config.py      # Configuration (SECRET_KEY, etc.)
│   ├── models.py      # Pydantic models
│   └── main.py        # Main FastAPI app
├── venv/              # Virtual environment (ignored by Git)
├── requirements.txt   # Dependencies
└── README.md          # Project documentation
```

## License
Project ini menggunakan lisensi MIT. Silakan lihat file LICENSE untuk informasi lebih lanjut.

## Authors
👨‍💻 Dibangun dengan ❤️ oleh kangcp.
