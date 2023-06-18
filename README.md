# Personal Loan Proposal Management System

To run the backend you must use `docker compose`

`docker compose up -d`

Next go to [Swagger Api doc](http://localhost:8000/api/docs/) in http://localhost:8000/api/docs/ for the api definitions and explication

- The program will load some data for testing like one user account.
- No authentication required for endpoints
- User credentials for [Django Admin](http://localhost:8000/api/admin/):

  - username: proposal_admin
  - password: proposal_admin

- Example Request:

  ```bash
  curl --request GET 'http://localhost:8000/api/v1/proposals/fields/' \
      --header 'Content-Type: application/json'

  ```

  - Example Response:
    `[{"uuid":"1c6f2eec-4d67-483d-8770-df22159e7de4","name":"CPF","slug":"cpf","type":"text","required":true,"is_active":true}]`

This project provide an API for managing loan proposals. It offers the following features:

- Get proposal fields
- Create a new loan proposal
- Background proposal analysis with Celery
- Django Admin Management Interface

## Test command

`docker compose run proposal_backend python3 manage.py test apps`
