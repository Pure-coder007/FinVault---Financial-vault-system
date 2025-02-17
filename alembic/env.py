from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
import os
from dotenv import load_dotenv
from wallet.database import Base

# Load environment variables
load_dotenv()

# Alembic Config object
config = context.config

# Fetch and set database URL
database_url = os.environ.get("SQLALCHEMY_DATABASE_URI")
if not database_url:
    raise ValueError("The environment variable 'SQLALCHEMY_DATABASE_URI' is not set.")
config.set_main_option("sqlalchemy.url", database_url)

# Set up logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Import all models to ensure Alembic detects them
from wallet.models import *  # Ensure all model files are imported

target_metadata = Base.metadata  # Assign correct metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(database_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
