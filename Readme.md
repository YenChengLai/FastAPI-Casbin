# Project Description

This project is trying to build RBAC (Role-Based Access Control) feature with fastAPI and Casbin, which will be a selected solution combination for the Operation Tool System for Zyxel Nebula Platform.

## Build up the environment

1. Go to the project folder in command line and run the below command:

    ```.sh
    ./init.sh
    ```

2. Activate the venv

    ```.sh
    source fastapi-casbin/bin/activate
    ```

## OP Tool Design

### Features

1. Role Management

2. Remote Device Access (SSH)

3. Email Communication (Sending emails)

4. Org/Site/Device Management

5. Firmware Management

6. Auditing

7. Announcement Management

### Roles

1. Administrator

2. Developer

3. User

### Feature - Role Relationship

| Feature                  | Administrator | Developer   | User        |
|--------------------------|---------------|-------------|-------------|
| Role Management          | ✓             |             |             |
| Remote Device Access     | ✓             |             | !           |
| Email Communication      | ✓             | ✓           |             |
| Organization Management  | ✓             | ✓           | ✓           |
| Firmware Management      | ✓             |             | !           |
| Auditing                 | ✓             |             |             |
| Announcement Management  | ✓             |             | !           |


