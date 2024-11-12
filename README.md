# GameStorm

## Project Overview

GameStorm API is a backend application designed to facilitate a gaming platform that integrates with the Lightning Network using the Zebedee API. The application allows users to authenticate, subscribe, and make payments via the Lightning Network, providing a seamless and secure gaming experience with cryptocurrency integration.

## Zebedee Integration

This project leverages the Zebedee API to interact with the Lightning Network. Zebedee provides a set of tools and services that enable developers to build Bitcoin Lightning applications, handling complex payment operations with ease.

## Getting a Zebedee API Key

To use the Zebedee API in this project, you need to obtain an API key. Follow these steps:

1. **Sign Up for a Zebedee Account**:
    - Visit the Zebedee Dashboard and create an account.
2. **Create a New Application**:
    - Once logged in, navigate to the Applications section.
    - Click on Create Application.
    - Fill in the required details for your application.
3. **Obtain the API Key**:
    - After creating the application, you will be provided with an API key.
    - Important: Keep this API key secure and do not expose it publicly.

## Configuring the Project with Environment Variables
To keep sensitive information secure and out of the codebase, the project uses environment variables to manage configuration settings like the Zebedee API key.

## Setting Up the `.env` File

1. **Create a `.env` File**:

In the `gamestorm-api` directory, create a file named `.env`.

```bash
cd gamestorm-api
touch .env
```

2. **Add Your API Key to the `.env` File**:

Open the `.env` file in a text editor and add the following line:

```env
ZEBEDEE_API_KEY=YOUR_ZEBEDEE_API_KEY
```

Replace `YOUR_ZEBEDEE_API_KEY` with the actual API key you obtained from Zebedee.

3. **Ensure the `.env` File is Ignored by Git**:

To prevent the `.env` file from being committed to version control (e.g., GitHub), add it to your `.gitignore` file.

**Add the following line to `.gitignore`**:

```bash
.env
```

4. Verify the Configuration in `config.py`:

The `gamestorm-api/gamestorm/config.py` file is set up to read the API key from the environment variable:

```python
# gamestorm-api/gamestorm/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # This loads the environment variables from the .env file

class Settings:
    """Configuration settings for the GameStorm application."""
    API_KEY = os.getenv("ZEBEDEE_API_KEY")  # Reads the API key from the environment
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gamestorm.db")

settings = Settings()
```

- The `load_dotenv()` function loads environment variables from the `.env` file.
- `os.getenv("ZEBEDEE_API_KEY")` retrieves the value of the `ZEBEDEE_API_KEY` environment variable.

## Project Status

The GameStorm API is currently in development. The core functionalities have been implemented, but some parts are still incomplete or contain placeholders (indicated by TODO comments in the code).

### Implemented Features

- User Authentication:
    - Users can authenticate using a username and Lightning Network address.
    - An invoice is generated for authentication purposes.
- Subscription Management:
    - Users can subscribe to the service by making a payment via the Lightning Network.
    - Subscription status can be queried to determine if a user is subscribed or unsubscribed.
- Payment Processing:
    - Integration with the Zebedee API to create charges and verify payments.

### Pending Implementations and TODOs

- Invoice Verification:
    - The verification of signed invoices in the `/authenticate/confirm` endpoint is not yet implemented.
    - **Files with TODOs**:
        - `gamestorm/routers/auth_router.py`
        - `gamestorm/utils/security.py`
- Security Enhancements:
    - Proper verification of payments and security checks need to be added.
- Error Handling and Validation:
    - Comprehensive error handling and input validation are required.
- Database Migrations:
    - Ensure that database migrations are properly managed with Alembic.

## Building and Running with Docker

The project includes a `Dockerfile` to build and run the GameStorm API using Docker.

### Prerequisites
- **Docker** installed on your machine.
- **Zebedee API Key** configured in a `.env` file.

### Steps to Build and Run

1. **Clone the Repository**:
```bash
git clone https://github.com/yourusername/gamestorm-api.git
cd gamestorm-api
```
2. **Set Up the `.env` File**:

Create a `.env` file and add your Zebedee API key:

```bash
echo "ZEBEDEE_API_KEY=YOUR_ZEBEDEE_API_KEY" > .env
```

Replace `YOUR_ZEBEDEE_API_KEY` with your actual API key.

3. **Ensure the `.env` File is in `.gitignore`**:

Confirm that the `.env` file is listed in `.gitignore` to prevent it from being committed to version control.

4. **Build the Docker Image**:

```bash
docker build -t gamestorm-api .
```

5. **Run the Docker Container**:

```bash
docker run -d -p 8000:8000 --env-file .env --name gamestorm-api gamestorm-api
```
- The API will be accessible at http://localhost:8000.
 
6. **Check the Logs (Optional)**:

```bash
docker logs -f gamestorm-api
```

7. **Stop and Remove the Container (Optional)**:

```bash
docker stop gamestorm-api
docker rm gamestorm-api
```

## API Endpoints Usage Examples
Below are examples of how to interact with the GameStorm API endpoints using `curl`.

### 1. User Authentication

**Endpoint:**
- `POST /authenticate`

**Request:**

```bash
curl -X POST "http://localhost:8000/authenticate" \
-H "Content-Type: application/json" \
-d '{
  "username": "user1",
  "ln_address": "user1@lnaddress.com"
}'
```

**Expected Response:**

```json
{
  "ln_invoice": "ln_invoice_for_user1@lnaddress.com",
  "user_id": 1
}
```

### 2. Confirm Authentication
**Endpoint:**
- `POST /authenticate/confirm`

**Note:** This endpoint is not fully implemented yet.

**Request:**

```bash
curl -X POST "http://localhost:8000/authenticate/confirm" \
-H "Content-Type: application/json" \
-d '{
  "signed_invoice": "signed_ln_invoice"
}'
```

**Expected Response:**

```json
{
  "status": "Authentication successful"
}
```

### 3. Check Subscription Status

**Endpoint:**
- `GET /subscriptionStatus`

**Request:**

```bash
curl -X GET "http://localhost:8000/subscriptionStatus" \
--data-urlencode "user_id=1"
```

**Expected Response:**

```json
{
  "status": "unsubscribed"
}
```

### 4. Subscribe User

**Endpoint:**
- `POST /subscribe`

**Request:**

```bash
curl -X POST "http://localhost:8000/subscribe" \
-H "Content-Type: application/json" \
-d '{
  "user_id": 1,
  "amount": 1000
}'
```

**Expected Response:**

```json
{
  "ln_invoice": "lnbc1... (actual Lightning invoice)",
  "charge_id": "charge_id_from_zebedee"
}
```

### 5. Verify Payment

**Endpoint:**
- `POST /verify-payment`

**Request:**

```bash
curl -X POST "http://localhost:8000/verify-payment" \
-H "Content-Type: application/json" \
-d '{
  "charge_id": "charge_id_from_zebedee",
  "user_id": 1
}'
```

**Expected Response:**

```json
{
  "status": "Subscription activated"
}
```

## Known Issues and Limitations

- **Incomplete Implementations**:
    - Invoice verification and security checks are pending.
    - Error handling and input validation need to be improved.
- **Testing**:
    - No unit tests or integration tests have been implemented yet.
- **Database Migrations**:
    - Ensure that Alembic migrations are correctly applied when making changes to models.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or improvements.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries or support, please contact:

Email: bitcynic@protonmail.com
GitHub: bitcynic