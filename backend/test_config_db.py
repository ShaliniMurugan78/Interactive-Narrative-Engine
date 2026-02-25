# test_config_db.py
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ---- Test config.py ----
print("=" * 40)
print("Testing config.py...")
print("=" * 40)

try:
    from app.config import (
        GROQ_API_KEY,
        HUGGINGFACE_API_KEY,
        MONGODB_URI,
        MONGODB_DB_NAME,
        MAX_TURNS,
        GROQ_MODEL
    )
    print(f"✅ GROQ_API_KEY     : {GROQ_API_KEY[:10]}...")
    print(f"✅ HUGGINGFACE_KEY  : {HUGGINGFACE_API_KEY[:10]}...")
    print(f"✅ MONGODB_DB_NAME  : {MONGODB_DB_NAME}")
    print(f"✅ GROQ_MODEL       : {GROQ_MODEL}")
    print(f"✅ MAX_TURNS        : {MAX_TURNS}")

except Exception as e:
    print(f"❌ config.py failed : {e}")


# ---- Test db.py ----
print()
print("=" * 40)
print("Testing db.py...")
print("=" * 40)

async def test_db():
    try:
        from app.database.db import connect_db, disconnect_db
        await connect_db()
        await disconnect_db()
        print("✅ Database test passed!")
    except Exception as e:
        print(f"❌ db.py failed: {e}")

asyncio.run(test_db())