import sys
import os

# Add backend directory to Python path so imports like
# "from db.database import ..." work inside Vercel serverless functions
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Set DATABASE_URL to /tmp for Vercel (read-only filesystem except /tmp)
if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:////tmp/agent_db.db"

from main import app
