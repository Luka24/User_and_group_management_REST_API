User and Group Management REST API Service
==========================================

This is a REST API service that provides a way to list, add, modify, and remove users and groups. Each user can belong to at most one group.
<br />


<br />

Data Model
----------

### Groups:

-   Name

### Users:

-   Email
-   Password
-   Name
-   Group

<br />

Endpoints
---------

### `GET /`

Returns a welcome message.

<br />

### `GET /groups`

Returns a list of all groups with their users.

Example response:

`{
    "groups": [
        {
            "id": 1,
            "name": "Group 1",
            "users": [
                {
                    "email": "user1@example.com",
                    "name": "User 1"
                },
                {
                    "email": "user2@example.com",
                    "name": "User 2"
                }
            ]
        },
        {
            "id": 2,
            "name": "Group 2",
            "users": [
                {
                    "email": "user3@example.com",
                    "name": "User 3"
                }
            ]
        }
    ]
}`


<br />

### `GET /groups/<id>`

Returns a specific group with its users.

Example response:

`{
    "id": 1,
    "name": "Group 1",
    "users": [
        {
            "email": "user1@example.com",
            "name": "User 1"
        },
        {
            "email": "user2@example.com",
            "name": "User 2"
        }
    ]
}`

<br />


### `POST /groups`

Creates a new group.

Example request:

`{
    "name": "New Group"
}`

Example response:


`{
    "id": 3
}`

<br />

### `PUT /groups/<id>`

Updates an existing group.

Example request:

`{
    "name": "Updated Group Name"
}`

Example response:

`{
    "message": "updated"
}`

<br />

### `DELETE /groups/<id>`

Deletes an existing group.

Example response:

`{
    "message": "deleted"
}`

<br />

### `GET /users`

Returns a list of all users.

Example response:

`{
    "users": [
        {
            "email": "user1@example.com",
            "password": "password1",
            "name": "User 1",
            "group_id": 1
        },
        {
            "email": "user2@example.com",
            "password": "password2",
            "name": "User 2",
            "group_id": 1
        },
        {
            "email": "user3@example.com",
            "password": "password3",
            "name": "User 3",
            "group_id": 2
        }
    ]
}`

<br />

### `GET /users/<id>`

Returns a specific user with their group.

Example response:


`{
    "name": "User 1",
    "email": "user1@example.com",
    "group": "Group 1"
}`

<br />

### `POST /users`

Creates a new user.

Example request:

`{
    "email": "user4@example.com",
    "password": "password4",
    "name": "User 4",
    "group_id": 2
}`

Example response:

`{
    "id": 4
}`

<br />

### `PUT /users/<id>`

Updates an existing user.

Example request:

`{
    "email": "user4@example.com",
    "password": "password4",
    "name": "User 4",
    "group_id": 2
}`

Example response:

`{
    "id": 4
}`

<br />

### `DELETE /users/<id>`

Deletes an existing user.

Example response:

`{
    "message": "deleted"
}`

<br />
