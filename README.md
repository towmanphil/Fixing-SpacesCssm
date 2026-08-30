# Fixing Spaces CMMS

## Deployment

This app is set up for a standard Python deployment using Flask + Gunicorn.

### Local development

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
# . .venv/bin/activate
pip install -r requirements.txt
python server.py
```

### Default login

The app seeds a default admin account for local use:

- Username: `admin`
- Password: `FixingSpaces123!`

You can change these with environment variables:

- `CMMS_ADMIN_USER`
- `CMMS_ADMIN_PASSWORD`
- `CMMS_SECRET_KEY`

### Production deployment options

- Render: use the included `render.yaml`
- Railway / Heroku-style hosts: use `Procfile`
- Docker: build with `docker build -t cmms .` and run `docker run -p 8000:8000 --env PORT=8000 cmms`
- Any container or VM: set `PORT` and run `gunicorn --bind 0.0.0.0:$PORT server:app`

### Environment variables

- `PORT`: port for the web server
- `CMMS_DB_PATH`: filesystem path for the SQLite database

### Deployment note

The app stores data in SQLite at `cmms.db` by default. On ephemeral hosting platforms, attach a persistent volume or set `CMMS_DB_PATH` to a durable storage location.
