# **Bookkeeping Application API Documentation**

## **Table of Contents**

- [Introduction](#introduction)
- [Authentication](#authentication)
  - [Login](#login)
  - [Logout](#logout)
  - [Get Current User](#get-current-user)
- [Accounts API](#accounts-api)
  - [List All Accounts](#list-all-accounts)
  - [Create a New Account](#create-a-new-account)
  - [Get an Account by ID](#get-an-account-by-id)
  - [Update an Account](#update-an-account)
  - [Delete an Account](#delete-an-account)
- [Transactions API](#transactions-api)
  - [List All Transactions](#list-all-transactions)
  - [Create a New Transaction](#create-a-new-transaction)
  - [Get a Transaction by ID](#get-a-transaction-by-id)
  - [Update a Transaction](#update-a-transaction)
  - [Delete a Transaction](#delete-a-transaction)
- [Error Handling](#error-handling)

---

## **Introduction**

The Bookkeeping Application provides a RESTful API for managing accounts and transactions. All API endpoints are prefixed with `/api` and require authentication unless specified otherwise.

---

## **Authentication**

### **Login**

- **Endpoint:** `/api/auth/login`
- **Method:** `POST`
- **Description:** Authenticate a user and establish a session.
- **Authentication Required:** No

#### **Request Body**

```json
{
  "username": "string",
  "password": "string"
}
```

- **Fields:**
  - `username` (string, required): The user's username.
  - `password` (string, required): The user's password.

#### **Response**

- **Status Code:** `200 OK`
- **Body:**

```json
{
  "id": 1,
  "username": "string",
  "role": "string"
}
```

#### **Example Request**

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass"
  }'
```

#### **Example Response**

```json
{
  "id": 1,
  "username": "testuser",
  "role": "User"
}
```

### **Logout**

- **Endpoint:** `/api/auth/logout`
- **Method:** `POST`
- **Description:** Log out the current user and end the session.
- **Authentication Required:** Yes

#### **Response**

- **Status Code:** `200 OK`
- **Body:**

```json
{
  "message": "Logged out successfully."
}
```

#### **Example Request**

```bash
curl -X POST http://localhost:5000/api/auth/logout
```

### **Get Current User**

- **Endpoint:** `/api/auth/user`
- **Method:** `GET`
- **Description:** Retrieve information about the currently authenticated user.
- **Authentication Required:** Yes

#### **Response**

- **Status Code:** `200 OK`
- **Body:**

```json
{
  "id": 1,
  "username": "string",
  "role": "string"
}
```

---

## **Accounts API**

### **List All Accounts**

- **Endpoint:** `/api/accounts/`
- **Method:** `GET`
- **Description:** Retrieve a list of all accounts.
- **Authentication Required:** Yes

#### **Response**

- **Status Code:** `200 OK`
- **Body:** Array of account objects.

```json
[
  {
    "id": 1,
    "name": "Cash",
    "type": "Asset"
  },
  {
    "id": 2,
    "name": "Revenue",
    "type": "Revenue"
  }
]
```

#### **Example Request**

```bash
curl -X GET http://localhost:5000/api/accounts/
```

### **Create a New Account**

- **Endpoint:** `/api/accounts/`
- **Method:** `POST`
- **Description:** Create a new account.
- **Authentication Required:** Yes

#### **Request Body**

```json
{
  "name": "string",
  "type": "string"
}
```

- **Fields:**
  - `name` (string, required): The account name.
  - `type` (string, required): The account type (e.g., Asset, Liability, Equity, Revenue, Expense).

#### **Response**

- **Status Code:** `201 Created`
- **Body:**

```json
{
  "id": 3,
  "name": "New Account",
  "type": "Asset"
}
```

#### **Example Request**

```bash
curl -X POST http://localhost:5000/api/accounts/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Account",
    "type": "Asset"
  }'
```

### **Get an Account by ID**

- **Endpoint:** `/api/accounts/{id}`
- **Method:** `GET`
- **Description:** Retrieve a specific account by its ID.
- **Authentication Required:** Yes

#### **Path Parameters**

- `id` (integer, required): The account ID.

#### **Response**

- **Status Code:** `200 OK`
- **Body:**

```json
{
  "id": 1,
  "name": "Cash",
  "type": "Asset"
}
```

#### **Example Request**

```bash
curl -X GET http://localhost:5000/api/accounts/1
```

### **Update an Account**

- **Endpoint:** `/api/accounts/{id}`
- **Method:** `PUT`
- **Description:** Update an existing account.
- **Authentication Required:** Yes

#### **Path Parameters**

- `id` (integer, required): The account ID.

#### **Request Body**

```json
{
  "name": "string",
  "type": "string"
}
```

- **Fields (at least one required):**
  - `name` (string, optional): The new account name.
  - `type` (string, optional): The new account type.

#### **Response**

- **Status Code:** `200 OK`
- **Body:**

```json
{
  "id": 1,
  "name": "Updated Account",
  "type": "Liability"
}
```

#### **Example Request**

```bash
curl -X PUT http://localhost:5000/api/accounts/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Account",
    "type": "Liability"
  }'
```

### **Delete an Account**

- **Endpoint:** `/api/accounts/{id}`
- **Method:** `DELETE`
- **Description:** Delete an account.
- **Authentication Required:** Yes

#### **Path Parameters**

- `id` (integer, required): The account ID.

#### **Response**

- **Status Code:** `204 No Content`

#### **Example Request**

```bash
curl -X DELETE http://localhost:5000/api/accounts/1
```

---

## **Transactions API**

### **List All Transactions**

- **Endpoint:** `/api/transactions/`
- **Method:** `GET`
- **Description:** Retrieve a list of all transactions.
- **Authentication Required:** Yes

#### **Response**

- **Status Code:** `200 OK`
- **Body:** Array of transaction objects.

```json
[
  {
    "id": 1,
    "date": "2023-11-07T12:00:00Z",
    "amount": 100.0,
    "description": "Sale",
    "debit_account_id": 1,
    "credit_account_id": 2
  }
]
```

#### **Example Request**

```bash
curl -X GET http://localhost:5000/api/transactions/
```

### **Create a New Transaction**

- **Endpoint:** `/api/transactions/`
- **Method:** `POST`
- **Description:** Create a new transaction.
- **Authentication Required:** Yes

#### **Request Body**

```json
{
  "date": "ISO8601 datetime string",
  "amount": number,
  "description": "string",
  "debit_account_id": integer,
  "credit_account_id": integer
}
```

- **Fields:**
  - `date` (string, required): The date of the transaction in ISO8601 format.
  - `amount` (number, required): The transaction amount.
  - `description` (string, required): Description of the transaction.
  - `debit_account_id` (integer, required): ID of the debit account.
  - `credit_account_id` (integer, required): ID of the credit account.

#### **Response**

- **Status Code:** `201 Created`
- **Body:**

```json
{
  "id": 2,
  "date": "2023-11-07T12:00:00Z",
  "amount": 150.0,
  "description": "Purchase",
  "debit_account_id": 3,
  "credit_account_id": 4
}
```

#### **Example Request**

```bash
curl -X POST http://localhost:5000/api/transactions/ \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2023-11-07T12:00:00Z",
    "amount": 150.0,
    "description": "Purchase",
    "debit_account_id": 3,
    "credit_account_id": 4
  }'
```

### **Get a Transaction by ID**

- **Endpoint:** `/api/transactions/{id}`
- **Method:** `GET`
- **Description:** Retrieve a specific transaction by its ID.
- **Authentication Required:** Yes

#### **Path Parameters**

- `id` (integer, required): The transaction ID.

#### **Response**

- **Status Code:** `200 OK`
- **Body:**

```json
{
  "id": 1,
  "date": "2023-11-07T12:00:00Z",
  "amount": 100.0,
  "description": "Sale",
  "debit_account_id": 1,
  "credit_account_id": 2
}
```

#### **Example Request**

```bash
curl -X GET http://localhost:5000/api/transactions/1
```

### **Update a Transaction**

- **Endpoint:** `/api/transactions/{id}`
- **Method:** `PUT`
- **Description:** Update an existing transaction.
- **Authentication Required:** Yes

#### **Path Parameters**

- `id` (integer, required): The transaction ID.

#### **Request Body**

```json
{
  "date": "ISO8601 datetime string",
  "amount": number,
  "description": "string",
  "debit_account_id": integer,
  "credit_account_id": integer
}
```

- **Fields (at least one required):**
  - `date` (string, optional): The new date of the transaction.
  - `amount` (number, optional): The new amount.
  - `description` (string, optional): The new description.
  - `debit_account_id` (integer, optional): The new debit account ID.
  - `credit_account_id` (integer, optional): The new credit account ID.

#### **Response**

- **Status Code:** `200 OK`
- **Body:**

```json
{
  "id": 1,
  "date": "2023-11-08T12:00:00Z",
  "amount": 120.0,
  "description": "Updated Sale",
  "debit_account_id": 1,
  "credit_account_id": 2
}
```

#### **Example Request**

```bash
curl -X PUT http://localhost:5000/api/transactions/1 \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 120.0,
    "description": "Updated Sale"
  }'
```

### **Delete a Transaction**

- **Endpoint:** `/api/transactions/{id}`
- **Method:** `DELETE`
- **Description:** Delete a transaction.
- **Authentication Required:** Yes

#### **Path Parameters**

- `id` (integer, required): The transaction ID.

#### **Response**

- **Status Code:** `204 No Content`

#### **Example Request**

```bash
curl -X DELETE http://localhost:5000/api/transactions/1
```

---

## **Error Handling**

The API uses standard HTTP status codes to indicate success or failure of API calls. The following are some common status codes and error responses.

### **Common Status Codes**

- `200 OK`: The request was successful.
- `201 Created`: A new resource was successfully created.
- `204 No Content`: The request was successful, and there is no additional content to send.
- `400 Bad Request`: The request was invalid or cannot be served.
- `401 Unauthorized`: Authentication is required and has failed or has not yet been provided.
- `403 Forbidden`: The request was valid, but you do not have the necessary permissions.
- `404 Not Found`: The requested resource could not be found.
- `500 Internal Server Error`: An error occurred on the server.

### **Error Response Format**

Error responses are returned in JSON format with a message describing the error.

#### **Example Error Response**

```json
{
  "message": "Invalid username or password."
}
```

---

## **Authentication Mechanism**

- The API uses session-based authentication managed by `Flask-Login`.
- Users must log in via the `/api/auth/login` endpoint to obtain a session.
- Subsequent requests must include the session cookie to be authenticated.

---

## **Notes**

- **Date Format:** All dates should be in ISO8601 format, e.g., `"2023-11-07T12:00:00Z"`.
- **Account Types:** Valid account types include `Asset`, `Liability`, `Equity`, `Revenue`, and `Expense`.
- **Data Validation:** Ensure all required fields are provided and valid to avoid `400 Bad Request` errors.

---

## **Contact**

For any questions or issues regarding the API, please contact the development team.

---

**End of API Documentation**

---
