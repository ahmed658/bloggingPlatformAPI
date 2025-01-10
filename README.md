# bloggingPlatformAPI

## Project Overview

This project is a RESTful API for a blogging platform designed with the following features:
- **User Authentication**: Secure user signup, login, and logout using JWT for authentication.
- **Blog Post Management**: Create, read, update, and delete (CRUD) operations for blog posts.
- **Comment Management**: CRUD operations for comments on blog posts.
- **Like Functionality**: Users can like blog posts and comments.
- **Database Management**: Uses SQLAlchemy ORM for managing database schema and operation

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


