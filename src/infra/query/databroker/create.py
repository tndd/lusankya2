def get_query_create_schema_databroker() -> str:
    return """
    CREATE SCHEMA IF NOT EXISTS databroker AUTHORIZATION postgres;
    """


def get_query_create_table_api_request() -> str:
    return """
    CREATE TABLE IF NOT EXISTS databroker.api_request (
        id uuid NOT NULL DEFAULT uuid_generate_v4(),
        time_stamp timestamptz NOT NULL DEFAULT now(),
        endpoint text NOT NULL,
        params json NOT NULL,
        req_header json NOT NULL,
        CONSTRAINT api_request_pkey PRIMARY KEY (id)
    );
    """


def get_query_create_table_api_response() -> str:
    return """
    CREATE TABLE IF NOT EXISTS databroker.api_response (
        id uuid NOT NULL DEFAULT uuid_generate_v4(),
        time_stamp timestamptz NOT NULL DEFAULT now(),
        request_id uuid NOT NULL,
        status int4 NOT NULL,
        resp_header json NOT NULL,
        body json NOT NULL,
        CONSTRAINT api_response_pkey PRIMARY KEY (id),
        CONSTRAINT api_response_fk FOREIGN KEY (request_id) REFERENCES databroker.api_request(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
    """
