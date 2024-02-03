CREATE TABLE IF NOT EXISTS databroker.api_response (
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	time_stamp timestamptz NOT NULL DEFAULT now(),
	api_request_id uuid NOT NULL,
	status int4 NOT NULL,
	resp_header json NOT NULL,
	body json NOT NULL,
	CONSTRAINT api_response_pkey PRIMARY KEY (id),
	CONSTRAINT api_response_fk FOREIGN KEY (api_request_id) REFERENCES databroker.api_request(id) ON DELETE CASCADE ON UPDATE CASCADE
);