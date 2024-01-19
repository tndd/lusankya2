CREATE TABLE IF NOT EXISTS dataflow.api_request (
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	time_stamp timestamptz NOT NULL DEFAULT now(),
	endpoint text NOT NULL,
	params json NOT NULL,
	req_header json NOT NULL,
	CONSTRAINT api_request_pkey PRIMARY KEY (id)
);