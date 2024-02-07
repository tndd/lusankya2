def get_query_create_extension_uuid() -> str:
    return """
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    """
