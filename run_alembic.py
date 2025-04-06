import os
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command

# Load environment variables from .env file
load_dotenv()

# Get the DATABASE_URL environment variable
database_url = os.getenv('DATABASE_URL')

# Ensure the DATABASE_URL is loaded correctly
if not database_url:
    raise ValueError("DATABASE_URL is not set in the .env file")

# Create an Alembic configuration object
alembic_config = Config("alembic.ini")

# Ensure 'sqlalchemy.url' is set in the Alembic configuration
alembic_config.set_section_option('alembic', 'sqlalchemy.url', database_url)

# Generate the migration script
try:
    # If you want to auto-generate migration script, use this
    command.revision(alembic_config, autogenerate=True, message="updated documents table to include chunk to help ID in pinecone")

    # After the migration script is generated, apply the migration
    command.upgrade(alembic_config, 'head')

    print("Migration completed successfully.")
except Exception as e:
    print(f"Error during migration: {e}")


