# bloggingPlatformAPI

## Project Overview

This project is a RESTful API for a blogging platform designed with the following features:
- **User Authentication**: Secure user signup, login, and logout using JWT for authentication.
- **Blog Post Management**: Create, read, update, and delete (CRUD) operations for blog posts.
- **Comment Management**: CRUD operations for comments on blog posts.
- **Like Functionality**: Users can like blog posts and comments.
- **Database Management**: Uses SQLAlchemy ORM for managing database schema and operation

In order to have this application service 1,000,000 users, I suggest making use of:
**Kubernetes** will ensure safe and automated rollouts of updates and the availability of containerized deployments as the Autoscaler can scale pods horizontally through CPU, memory, or application metrics as the number of requests received. 
Runing the application in **multi-AZs** for failover and low-latency deployment. 

**AWS ELB** should be used to well distribute traffic across Kubernetes nodes to avoid some nodes getting congested with traffic.

Add **Redis** as the caching layer in order to decrease the amount of calls to the database and increase performance for frequently requested data, with examples including user sessions and API responses. In terms of broad horizontal scalability and availability, the team should begin to set up **Redis Cluster**.
For the database, I recommend **Amazon RDS with PostgreSQL** which is a managed service that helps in easy database hosting and maintenance by replicating the primary database to a master database that can now easily handle all the write traffic. To improve the performance of the database, we can use indexing, query optimization, and partitioning techniques. These, combined with **Redis caching** will reduce the need for frequent database lookups for such data.

Utilize Kubernetes Horizontal Pod Autoscalers (HPA) for both application pods and Redis cluster nodes to dynamically adjust based on traffic. 
Leverage AWS Auto Scaling Groups to automatically scale and monitor system performance using tools like **Prometheus** and Grafana, enabling proactive issue detection and efficient resource allocation with the use of cloud metrics and actions.

## Technologies and Libraries Used

The application leverages a modern tech stack to ensure scalability, reliability, and high performance. Below is an overview of the key technologies and libraries used:

### Backend
- **FastAPI**: A modern, high-performance web framework for building APIs with Python 3.9+.
- **SQLAlchemy**: An ORM (Object Relational Mapper) for database interactions.
- **Alembic**: A database migration tool for SQLAlchemy
- **Pydantic**: Used for data validation and settings management.
- **Passlib & bcrypt**: For password hashing and security.
- **PyJWT**: For JSON Web Token (JWT) authentication.

### Database
- **PostgreSQL**: A powerful, open-source relational database for storing application data.

### Testing
- **pytest**: A framework for writing and running unit tests to ensure application reliability.

### Additional Libraries
- **psycopg2-binary**: PostgreSQL database adapter for Python.
- **pydantic-extra-types**: Provides extended data types like phone numbers for validation.
- **phonenumbers**: Library for parsing and validating phone numbers.


# Setting Up the Project

Follow these steps to configure and run the project locally.

---

## 1. Prerequisites

- **Python 3.9+**: Ensure you have Python installed on your machine. You can download it [here](https://www.python.org/downloads/).
- **PostgreSQL**: Install PostgreSQL and set up a database.

---

## 2. Clone the Repository

Clone this repository to your local machine:

```bash
git clone <repository-url>
cd <repository-folder>
```

---

## 3. Install Dependencies

Install the required Python dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

The project uses a `.env` file to manage sensitive settings. Create a `.env` file in the root directory and populate it with the following content:

```env
DATABASE_HOSTNAME="localhost"
DATABASE_NAME="blogDB"
database_port="5432"
database_username="postgres"
database_password="password"
secret_key="2b0c852c5a7ec6feff08f3031b37c5aa071291aa77f703059efdee8342bb24a0"
algorithm="HS256"
access_token_expire_minutes=60
root_pass="useThisPassToBeAbleToCreateAdminUsers"
```

### Customizing `.env`

- Update `DATABASE_HOSTNAME`, `DATABASE_NAME`, `database_username`, `database_password`, and `database_port` based on your PostgreSQL setup.
- Keep the `secret_key` secure and avoid sharing it publicly.
- Modify `access_token_expire_minutes` if needed for token expiration duration.

---

## 5. Initialize the Database

Before running the app, ensure your PostgreSQL database is set up and ready:

1. Log in to PostgreSQL and create a database:
   ```sql
   CREATE DATABASE blogDB;
   ```
2. Verify the `.env` file matches your PostgreSQL credentials and database name.

---

## 6. Set Up the Database
   Initialize the database by applying Alembic migrations:

   - **Upgrade the Database:**
     ```bash
     alembic upgrade head
     ```

   - **Alembic Initial Migration Details:**
     - Tables created: `users`, `blog_posts`, `comments`, `posts_likes`, `comments_likes`.
     - Relationships:
       - `users` table has relationships with `blog_posts`, `comments`, `posts_likes`, and `comments_likes`.
       - `blog_posts` table has relationships with `users`, `comments`, and `posts_likes`.
       - `comments` table has relationships with `users`, `blog_posts`, and `comments_likes`.

   - **Rollback (if needed):**
     ```bash
     alembic downgrade -1
     ```

## 7. Run the Application
   Start the FastAPI application:
   ```bash
   uvicorn app.main:blogApp --reload
   ```

   The app will be available at `http://127.0.0.1:8000`.

---

### Summary of Alembic Migration
- **Initial Migration ID:** `10240b4e307f`
- **Tables Created:** `users`, `blog_posts`, `comments`, `posts_likes`, and `comments_likes`.
- **Commands:**
  - Upgrade: `alembic upgrade head`
  - Downgrade: `alembic downgrade -1`

---

This ensures that your application is set up with proper database migrations and ready to run.

---

## 8. Postman Collection and Environment

This project includes a Postman collection and environment to simplify API testing. You can find these files in the `postman` folder:

- **Postman Collection**: `bloggingPlatformAPI.postman_collection.json`  
  Contains all the endpoints for testing the APIs.

- **Postman Environment**: `Blog Platform Env.postman_environment.json`  
  Pre-configured environment variables for API testing.

### Using Postman
1. Open Postman.
2. Import the collection and environment files:
   - Go to **File > Import**.
   - Select the JSON files from the `postman` folder.
3. Set the active environment to **Blog Platform Env**.
4. Start testing the API endpoints.

---

## 9. Running Tests

The project includes unit tests written with `pytest`. To run the tests, execute:

```bash
pytest
```

---

## Troubleshooting

1. **Database Connection Errors**: Verify your `.env` file and PostgreSQL setup.
2. **Dependency Issues**: Ensure all dependencies are installed using `pip install -r requirements.txt`.
3. **Application Port Conflict**: Check if another application is using port `8000`.

---

You’re now ready to use the application! 🎉

# API Documentation:

## Users Module

## Overview
The **Users Module** provides a comprehensive set of endpoints for managing user accounts, including user registration, authentication, profile updates, and administrative user management. This module also supports role-based access control, allowing differentiation between regular users and administrators.

---

## Endpoints

### 1. Register a User
**Method:** `POST`

**URL:** `{{URL}}/users`

**Description:** Allows the creation of a new user account.

**Implementation Details:**
- Validates admin user creation with the correct root password.
- Hashes the user password before saving.
- Removes any `root_pass` attribute from non-admin users.
- Handles potential database conflicts (e.g., duplicate entries).

**Request Body:**
```json
{
    "username": "gammaassets-user",
    "password": "password-for-gammaassets-user",
    "first_name": "ahmed3",
    "last_name": "maher",
    "email": "ahmedmaherbf23@gmail.com"
}
```

**Response:**
- **201 Created:** User successfully registered.
  ```json
  {
      "user_id": 1,
      "username": "gammaassets-user",
      "first_name": "ahmed3",
      "last_name": "maher",
      "email": "ahmedmaherbf23@gmail.com",
      "admin": false
  }
  ```

**Schemas:**
- **Request:** `UserCreate`
- **Response:** `UserOut`

---

### 2. Edit Current User
**Method:** `PUT`

**URL:** `{{URL}}/users`

**Description:** Allows a user to update their profile details.

**Implementation Details:**
- Requires user authentication.
- Updates only provided fields, leaving others unchanged.
- Hashes password if updated.
- Uses `synchronize_session=False` for efficiency when updating.

**Headers:**
- **Authorization:** `Bearer <JWT Token>`

**Request Body:**
```json
{
    "first_name": "Edited First Name",
    "phone": "+201001776665"
}
```

**Response:**
- **200 OK:** User profile updated successfully.
  ```json
  {
      "user_id": 1,
      "username": "gammaassets-user",
      "first_name": "Edited First Name",
      "last_name": "maher",
      "email": "ahmedmaherbf23@gmail.com",
      "admin": false,
      "phone": "tel:+20-10-01776665"
  }
  ```

**Schemas:**
- **Request:** `UserEdit`
- **Response:** `UserOut`

---

### 3. Login User
**Method:** `POST`

**URL:** `{{URL}}/login`

**Description:** Authenticates a user and returns a JWT token.

**Request Body (Form Data):**
- `username`: `gammaassets-user`
- `password`: `password-for-gammaassets-user`

**Response:**
- **200 OK:** Authentication successful.
  ```json
  {
      "access_token": "eyJhb...",
      "token_type": "bearer"
  }
  ```

**Schemas:**
- **Response:** `Token`

---

### 4. Register an Admin
**Method:** `POST`

**URL:** `{{URL}}/users`

**Description:** Allows the creation of an admin account. Requires a root password.

**Implementation Details:**
- Validates the root password for admin creation.
- Ensures proper password hashing.
- Removes the `root_pass` attribute before saving.

**Request Body:**
```json
{
    "username": "admin1",
    "email": "admin@gammaassets.com",
    "password": "adminPassword",
    "first_name": "Gamma",
    "last_name": "Maher",
    "admin": true,
    "root_pass": "useThisPassToBeAbleToCreateAdminUsers"
}
```

**Response:**
- **201 Created:** Admin successfully registered.
  ```json
  {
      "user_id": 2,
      "username": "admin1",
      "first_name": "Gamma",
      "last_name": "Maher",
      "email": "admin@gammaassets.com",
      "admin": true
  }
  ```

**Schemas:**
- **Request:** `UserCreate`
- **Response:** `UserOut`

---

### 5. List All Users (Admin Only)
**Method:** `GET`

**URL:** `{{URL}}/users`

**Description:** Retrieves a list of all registered users. Only accessible by admins.

**Implementation Details:**
- Verifies that the current user has admin privileges.
- Queries all users in the database.

**Headers:**
- **Authorization:** `Bearer <Admin JWT Token>`

**Response:**
- **200 OK:** List of users.
  ```json
  [
      {
          "user_id": 1,
          "username": "gammaassets-user",
          "first_name": "ahmed3",
          "last_name": "maher",
          "email": "ahmedmaherbf23@gmail.com",
          "admin": false
      },
      {
          "user_id": 2,
          "username": "admin1",
          "first_name": "Gamma",
          "last_name": "Maher",
          "email": "admin@gammaassets.com",
          "admin": true
      }
  ]
  ```

**Schemas:**
- **Response:** `List[UserOut]`

---

### 6. Delete Current User
**Method:** `DELETE`

**URL:** `{{URL}}/users`

**Description:** Deletes the currently authenticated user.

**Implementation Details:**
- Requires user credentials for verification.
- Deletes the user from the database if authenticated.

**Request Body (Form Data):**
- `username`: `gammaassets-user`
- `password`: `password-for-gammaassets-user`

**Response:**
- **204 No Content:** User successfully deleted.

---

### 7. Delete Another User (Admin Only)
**Method:** `DELETE`

**URL:** `{{URL}}/users/{username}`

**Description:** Deletes another user's account. Only accessible by admins.

**Implementation Details:**
- Verifies admin privileges.
- Deletes the specified user from the database.
- Handles non-existent user errors.

**Headers:**
- **Authorization:** `Bearer <Admin JWT Token>`

**Response:**
- **204 No Content:** User successfully deleted.

**Schemas:**
- **Response:** None

---

## Models

### User Schema
```python
class UserSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    admin: Optional[bool] = False
    birthdate: Optional[date] = None
    phone: Optional[PhoneNumber] = None
```

### User Create Schema
```python
class UserCreate(UserSchema):
    password: str
    root_pass: Optional[str] = None
```

### User Output Schema
```python
class UserOut(UserSchema):
    user_id: int
```

### User Edit Schema
```python
class UserEdit(BaseModel):
    username: Optional[str] = None   
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    birthdate: Optional[date] = None
    phone: Optional[PhoneNumber] = None
    password: Optional[str] = None
```

---

## Posts Module Endpoints

### 1. Create a Post
**Method:** `POST`

**URL:** `{{URL}}/posts`

**Description:** Allows authenticated users to create a new blog post.

**Implementation Details:**
- Associates the post with the currently authenticated user.
- Adds the new post to the database and refreshes it for the response.

**Request Body:**

```json
{
    "title": "Sample Post Title",
    "content": "This is the content of the sample post."
}
```

**Response:**

- **201 Created:** Post successfully created.
  ```json
  {
      "post_id": 1,
      "title": "Sample Post Title",
      "content": "This is the content of the sample post.",
      "created_at": "2025-01-11T00:00:00",
      "updated_at": "2025-01-11T00:00:00",
      "like_count": 0,
      "author": {
          "username": "user1",
          "first_name": "John",
          "last_name": "Doe"
      }
  }
  ```

**Schemas:**
- **Request:** `PostCreate`
- **Response:** `PostReturn`

---

### 2. Retrieve Posts
**Method:** `GET`

**URL:** `{{URL}}/posts`

**Description:** Retrieves a list of posts with optional search and pagination.

**Implementation Details:**

- Supports searching by content.
- Supports pagination using `limit` and `skip` query parameters.

**Query Parameters:**

- `limit`: Maximum number of posts to return (default: 10).
- `skip`: Number of posts to skip (default: 0).
- `search`: Search term for post content (optional).

**Response:**

- **200 OK:** List of posts.
  ```json
  [
      {
          "post_id": 1,
          "title": "Sample Post Title",
          "content": "This is the content of the sample post.",
          "created_at": "2025-01-11T00:00:00",
          "updated_at": "2025-01-11T00:00:00",
          "like_count": 0,
          "author": {
              "username": "user1",
              "first_name": "John",
              "last_name": "Doe"
          }
      }
  ]
  ```

**Schemas:**

- **Response:** `List[PostReturn]`

---

### 3. Retrieve a Single Post
**Method:** `GET`

**URL:** `{{URL}}/posts/{id}`

**Description:** Retrieves the details of a specific post by its ID.

**Implementation Details:**

- Validates that the post exists.

**Response:**

- **200 OK:** Post details.
- **404 Not Found:** Post with the given ID does not exist.

**Schemas:**

- **Response:** `PostReturn`

---

### 4. Update a Post
**Method:** `PUT`

**URL:** `{{URL}}/posts/{id}`

**Description:** Allows the author of a post to update its title and content.

**Implementation Details:**

- Verifies that the post exists and belongs to the current user.
- Updates the post with the provided data.

**Request Body:**

```json
{
    "title": "Updated Post Title",
    "content": "Updated content."
}
```

**Response:**

- **200 OK:** Post successfully updated.
- **403 Forbidden:** Post does not belong to the current user.
- **404 Not Found:** Post does not exist.

**Schemas:**

- **Request:** `PostCreate`
- **Response:** `PostReturn`

---

### 5. Delete a Post
**Method:** `DELETE`

**URL:** `{{URL}}/posts/{id}`

**Description:** Allows the author of a post to delete it.

**Implementation Details:**

- Verifies that the post exists and belongs to the current user.

**Response:**

- **204 No Content:** Post successfully deleted.
- **403 Forbidden:** Post does not belong to the current user.
- **404 Not Found:** Post does not exist.

---


### PostCreate Schema

```python
class PostCreate(BaseModel):
    title: str
    content: str
```

### PostReturn Schema

```python
class PostReturn(PostBase):
    post_id: int
    created_at: datetime
    updated_at: datetime
    like_count: int
    author: UserOutPublic
```

## Authentication Module Endpoints

### 1. User Login
**Method:** `POST`

**URL:** `{{URL}}/login`

**Description:** Authenticates a user and generates a JWT token for accessing protected resources.

**Implementation Details:**
- Validates user credentials (username and password).
- Verifies the password against the stored hash.
- Generates a JWT token containing the user ID and expiration time.

**Request Body (Form Data):**
```json
{
    "username": "gammaassets-user",
    "password": "password-for-gammaassets-user"
}
```

**Response:**
- **200 OK:** Login successful.
  ```json
  {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer"
  }
  ```

**Error Responses:**
- **403 Forbidden:** Invalid credentials provided.

**Schemas:**
- **Response:** `Token`

---

## Authentication Module Endpoints

### 1. User Login
**Method:** `POST`

**URL:** `{{URL}}/login`

**Description:** Authenticates a user and generates a JWT token for accessing protected resources.

**Implementation Details:**
- Validates user credentials (username and password).
- Verifies the password against the stored hash.
- Generates a JWT token containing the user ID and expiration time.

**Request Body (Form Data):**
```json
{
    "username": "gammaassets-user",
    "password": "password-for-gammaassets-user"
}
```

**Response:**
- **200 OK:** Login successful.
  ```json
  {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer"
  }
  ```

**Error Responses:**
- **403 Forbidden:** Invalid credentials provided.

**Schemas:**
- **Response:** `Token`

---

## Authentication Services

### 1. JWT Token Creation
**Function:** `create_jwt_token`

**Description:** Generates a JWT token containing user data and expiration information.

**Implementation:**
```python
def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### 2. Verify Access Token
**Function:** `verify_access_token`

**Description:** Decodes and validates the JWT token, ensuring it is correctly formed and unexpired.

**Implementation:**
```python
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return schemas.TokenData(id=user_id)
    except InvalidTokenError:
        raise credentials_exception
```

### 3. Get Current User
**Function:** `get_current_user`

**Description:** Retrieves the currently authenticated user based on the provided JWT token.

**Implementation:**
```python
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = verify_access_token(token, credentials_exception).id
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise credentials_exception
    return user
```

---

## Example Usage

### Login Request
**Request:**
```http
POST /login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=exampleuser&password=examplepassword
```

**Response:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### Accessing a Protected Resource
**Request:**
```http
GET /protected-resource HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
    "message": "Access granted"
}
```
---

## Error Responses

### 1. Invalid Credentials
**HTTP Status Code:** `403 Forbidden`

**Description:** Raised when the username or password provided during login is incorrect.

**Response Example:**
```json
{
    "detail": "Invalid credentials"
}
```

---

### 2. Token Validation Failure
**HTTP Status Code:** `401 Unauthorized`

**Description:** Raised when the provided JWT token is invalid, expired, or missing required claims.

**Response Example:**
```json
{
    "detail": "Could not validate credentials"
}
```

---

## Models

### 1. Token Schema
**Purpose:** Represents the JWT token returned upon successful authentication.

```python
class Token(BaseModel):
    access_token: str
    token_type: str
```

### 2. TokenData Schema
**Purpose:** Represents the data extracted from a verified JWT token.

```python
class TokenData(BaseModel):
    id: Optional[int] = None
```

---

## Security and Best Practices

1. **Password Hashing:**
   - User passwords are hashed before being stored in the database.
   - Use a secure hashing algorithm (e.g., bcrypt).

2. **Token Expiry:**
   - JWT tokens include an expiration time (`exp`) to limit their validity period.
   - Refresh tokens can be implemented for long-term access if required.

3. **HTTPS:**
   - Ensure the application is deployed over HTTPS to protect sensitive data during transmission.

4. **Bearer Token Format:**
   - Tokens are transmitted using the `Authorization` header in the format: `Bearer <token>`.

5. **Error Handling:**
   - Detailed error messages should not reveal sensitive information.
   - Use standard HTTP status codes for consistency.

---

## Example Usage

### Login Request
**Request:**
```http
POST /login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=exampleuser&password=examplepassword
```

**Response:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### Accessing a Protected Resource
**Request:**
```http
GET /protected-resource HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
    "message": "Access granted"
}
```
# API Documentation: Comments Module

## Overview
The **Comments Module** provides a set of endpoints for managing comments on blog posts. Users can create, retrieve, update, and delete comments. The module ensures that only the owner of a comment can modify or delete it, providing secure and controlled access.

---

## Comments Module

## Endpoints

### 1. Create a Comment
**Method:** `POST`

**URL:** `{{URL}}/comments/posts/{post_id}`

**Description:** Adds a new comment to a specified blog post.

**Implementation Details:**
- Verifies that the blog post exists.
- Associates the comment with the current authenticated user and the specified post.

**Path Parameters:**
- `post_id`: The ID of the blog post to comment on.

**Request Body:**
```json
{
    "content": "This is a comment."
}
```

**Response:**
- **201 Created:** Comment successfully added.
  ```json
  {
      "comment_id": 1,
      "blog_post_id": 123,
      "content": "This is a comment.",
      "created_at": "2025-01-11T10:00:00Z",
      "updated_at": "2025-01-11T10:00:00Z",
      "like_count": 0,
      "author": {
          "username": "user123",
          "first_name": "John",
          "last_name": "Doe"
      }
  }
  ```

**Schemas:**
- **Request:** `CommentCreate`
- **Response:** `CommentReturn`

---

### 2. Retrieve Comments for a Blog Post
**Method:** `GET`

**URL:** `{{URL}}/comments/posts/{post_id}`

**Description:** Retrieves a list of comments for a specified blog post, with optional pagination.

**Path Parameters:**
- `post_id`: The ID of the blog post to retrieve comments for.

**Query Parameters:**
- `limit`: The maximum number of comments to retrieve (default: 10).
- `skip`: The number of comments to skip (default: 0).

**Response:**
- **200 OK:** List of comments for the specified post.
  ```json
  [
      {
          "comment_id": 1,
          "blog_post_id": 123,
          "content": "This is a comment.",
          "created_at": "2025-01-11T10:00:00Z",
          "updated_at": "2025-01-11T10:00:00Z",
          "like_count": 0,
          "author": {
              "username": "user123",
              "first_name": "John",
              "last_name": "Doe"
          }
      }
  ]
  ```

**Schemas:**
- **Response:** `List[CommentReturn]`

---

### 3. Retrieve a Single Comment
**Method:** `GET`

**URL:** `{{URL}}/comments/{id}`

**Description:** Retrieves the details of a specific comment by its ID.

**Path Parameters:**
- `id`: The ID of the comment to retrieve.

**Response:**
- **200 OK:** The details of the comment.
  ```json
  {
      "comment_id": 1,
      "blog_post_id": 123,
      "content": "This is a comment.",
      "created_at": "2025-01-11T10:00:00Z",
      "updated_at": "2025-01-11T10:00:00Z",
      "like_count": 0,
      "author": {
          "username": "user123",
          "first_name": "John",
          "last_name": "Doe"
      }
  }
  ```

**Schemas:**
- **Response:** `CommentReturn`

---

### 4. Update a Comment
**Method:** `PUT`

**URL:** `{{URL}}/comments/{id}`

**Description:** Updates the content of an existing comment. Only the owner of the comment can perform this action.

**Path Parameters:**
- `id`: The ID of the comment to update.

**Request Body:**
```json
{
    "content": "Updated comment content."
}
```

**Response:**
- **200 OK:** The updated comment.
  ```json
  {
      "comment_id": 1,
      "blog_post_id": 123,
      "content": "Updated comment content.",
      "created_at": "2025-01-11T10:00:00Z",
      "updated_at": "2025-01-11T11:00:00Z",
      "like_count": 0,
      "author": {
          "username": "user123",
          "first_name": "John",
          "last_name": "Doe"
      }
  }
  ```

**Schemas:**
- **Request:** `CommentCreate`
- **Response:** `CommentReturn`

---

### 5. Delete a Comment
**Method:** `DELETE`

**URL:** `{{URL}}/comments/{id}`

**Description:** Deletes a specific comment. Only the owner of the comment can perform this action.

**Path Parameters:**
- `id`: The ID of the comment to delete.

**Response:**
- **204 No Content:** Comment successfully deleted.

---

## Error Responses

### 1. Blog Post Not Found
**HTTP Status Code:** `404 Not Found`

**Description:** Raised when the specified blog post ID does not exist.

**Response Example:**
```json
{
    "detail": "Blog post with ID 123 was not found."
}
```

### 2. Comment Not Found
**HTTP Status Code:** `404 Not Found`

**Description:** Raised when the specified comment ID does not exist.

**Response Example:**
```json
{
    "detail": "Comment with ID 1 was not found."
}
```

### 3. Forbidden Action
**HTTP Status Code:** `403 Forbidden`

**Description:** Raised when a user attempts to update or delete a comment they do not own.

**Response Example:**
```json
{
    "detail": "Comment with ID 1 doesn't belong to the current user."
}
```

---

## Models

### CommentCreate Schema
```python
class CommentCreate(BaseModel):
    content: str
```

### CommentReturn Schema
```python
class CommentReturn(BaseModel):
    comment_id: int
    blog_post_id: int
    content: str
    created_at: datetime
    updated_at: datetime
    like_count: int
    author: UserOutPublic
```

---

## Security and Best Practices

1. **User Authentication:**
   - Endpoints require the user to be authenticated via JWT tokens.

2. **Authorization:**
   - Only the owner of a comment can update or delete it.

3. **Error Handling:**
   - Detailed error messages are provided for invalid actions or non-existent resources.

4. **Pagination:**
   - Use `limit` and `skip` query parameters for efficient retrieval of comments on a blog post.
---


## Likes Module

## Overview
The **Likes Module** provides endpoints to manage likes on blog posts and comments. Users can like or unlike posts and comments and retrieve a list of users who have liked a specific post or comment. The module ensures proper validation and prevents duplicate actions (e.g., liking the same post twice).

---

## Endpoints

### 1. Like a Post
**Method:** `POST`

**URL:** `{{URL}}/likes/posts/{post_id}`

**Description:** Adds a like to a specified blog post.

**Implementation Details:**
- Checks if the blog post exists.
- Ensures the user has not already liked the post.
- Increments the like count for the post.

**Path Parameters:**
- `post_id`: The ID of the blog post to like.

**Response:**
- **201 Created:** Post successfully liked.
  ```json
  {
      "message": "Post 1 liked successfully.",
      "like_count": 10
  }
  ```

**Schemas:**
- **Response:** `PostLikeResponse`

---

### 2. Unlike a Post
**Method:** `DELETE`

**URL:** `{{URL}}/likes/posts/{post_id}`

**Description:** Removes a like from a specified blog post.

**Implementation Details:**
- Checks if the blog post exists.
- Ensures the user has previously liked the post.
- Decrements the like count for the post.

**Path Parameters:**
- `post_id`: The ID of the blog post to unlike.

**Response:**
- **200 OK:** Post successfully unliked.
  ```json
  {
      "message": "Post 1 unliked successfully.",
      "like_count": 9
  }
  ```

**Schemas:**
- **Response:** `PostLikeResponse`

---

### 3. Like a Comment
**Method:** `POST`

**URL:** `{{URL}}/likes/comments/{comment_id}`

**Description:** Adds a like to a specified comment.

**Implementation Details:**
- Checks if the comment exists.
- Ensures the user has not already liked the comment.
- Increments the like count for the comment.

**Path Parameters:**
- `comment_id`: The ID of the comment to like.

**Response:**
- **201 Created:** Comment successfully liked.
  ```json
  {
      "message": "Comment 1 liked successfully.",
      "like_count": 5
  }
  ```

**Schemas:**
- **Response:** `CommentLikeResponse`

---

### 4. Unlike a Comment
**Method:** `DELETE`

**URL:** `{{URL}}/likes/comments/{comment_id}`

**Description:** Removes a like from a specified comment.

**Implementation Details:**
- Checks if the comment exists.
- Ensures the user has previously liked the comment.
- Decrements the like count for the comment.

**Path Parameters:**
- `comment_id`: The ID of the comment to unlike.

**Response:**
- **200 OK:** Comment successfully unliked.
  ```json
  {
      "message": "Comment 1 unliked successfully.",
      "like_count": 4
  }
  ```

**Schemas:**
- **Response:** `CommentLikeResponse`

---

### 5. Get Users Who Liked a Post
**Method:** `GET`

**URL:** `{{URL}}/likes/posts/{post_id}/users`

**Description:** Retrieves a list of users who liked a specified blog post.

**Path Parameters:**
- `post_id`: The ID of the blog post.

**Query Parameters:**
- `limit`: The maximum number of users to retrieve (default: 10).
- `skip`: The number of users to skip (default: 0).

**Response:**
- **200 OK:** List of users who liked the post.
  ```json
  [
      {
          "username": "user123",
          "first_name": "John",
          "last_name": "Doe"
      },
      {
          "username": "user456",
          "first_name": "Jane",
          "last_name": "Smith"
      }
  ]
  ```

**Schemas:**
- **Response:** `List[UserOutPublic]`

---

### 6. Get Users Who Liked a Comment
**Method:** `GET`

**URL:** `{{URL}}/likes/comments/{comment_id}/users`

**Description:** Retrieves a list of users who liked a specified comment.

**Path Parameters:**
- `comment_id`: The ID of the comment.

**Query Parameters:**
- `limit`: The maximum number of users to retrieve (default: 10).
- `skip`: The number of users to skip (default: 0).

**Response:**
- **200 OK:** List of users who liked the comment.
  ```json
  [
      {
          "username": "user123",
          "first_name": "John",
          "last_name": "Doe"
      },
      {
          "username": "user456",
          "first_name": "Jane",
          "last_name": "Smith"
      }
  ]
  ```

**Schemas:**
- **Response:** `List[UserOutPublic]`

---

## Error Responses

### 1. Resource Not Found
**HTTP Status Code:** `404 Not Found`

**Description:** Raised when the specified post or comment does not exist.

**Response Example:**
```json
{
    "detail": "Post with ID 1 does not exist."
}
```

### 2. Already Liked
**HTTP Status Code:** `409 Conflict`

**Description:** Raised when the user tries to like a post or comment they have already liked.

**Response Example:**
```json
{
    "detail": "You have already liked post 1."
}
```

### 3. Not Liked
**HTTP Status Code:** `404 Not Found`

**Description:** Raised when the user tries to unlike a post or comment they have not previously liked.

**Response Example:**
```json
{
    "detail": "You haven't liked post 1."
}
```

---

## Models

### PostLikeResponse Schema
```python
class PostLikeResponse(BaseModel):
    message: str
    like_count: int
```

### CommentLikeResponse Schema
```python
class CommentLikeResponse(BaseModel):
    message: str
    like_count: int
```

### UserOutPublic Schema
```python
class UserOutPublic(BaseModel):
    username: str
    first_name: str
    last_name: str
```

---

## Security and Best Practices

1. **User Authentication:**
   - Endpoints require user authentication via JWT tokens.

2. **Duplicate Prevention:**
   - Validates actions to prevent duplicate likes or unlikes.

3. **Error Handling:**
   - Detailed error messages ensure proper feedback for invalid actions.

4. **Pagination:**
   - Use `limit` and `skip` query parameters for efficient retrieval of users who liked a post or comment.
