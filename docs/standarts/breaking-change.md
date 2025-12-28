# Breaking Change

A change is **breaking** if existing clients or integrations stop working without updates.

## HTTP API
- Remove or rename an endpoint.
- Change the HTTP method or URL.
- Add required parameters or fields.
- Remove/rename fields or change their type/format in requests or responses.
- Change HTTP status codes or the error format.
- Change authentication/authorization so previously valid access no longer works.

## Database / data
- Remove or rename tables or columns.
- Change column type, `NULL`/`NOT NULL`, constraints, or enum values.
- Change data meaning (units, formats, semantics).

## Integrations (events, webhooks, exports)
- Remove or rename topics, queues, webhooks, or exports.
- Remove/rename fields or change message type/format.
- Change delivery or retry guarantees.

## Configuration / operations
- Remove or rename environment variables or config keys.
- Make previously optional configuration required.
- Incompatible changes to CLI, ports, entrypoint, or healthcheck paths.
