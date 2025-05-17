# Legal User Management System

A Django REST Framework-based backend system for managing legal users, including clients, attorneys, and administrators.

## Features

- User Authentication with JWT
- Role-based Access Control (Admin, Attorney, Client)
- OTP-based Email Verification
- User Profile Management
- Attorney Profile Management
- Client Profile Management
- Admin Dashboard

## Tech Stack

- Python 3.12
- Django 5.1.3
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Simple JWT

## Prerequisites

- Python 3.12 or higher
- PostgreSQL
- pip (Python package manager)
- virtualenv (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/main-backend.git
cd main-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## API Documentation

### Authentication Endpoints

#### Login
- **POST** `/api/login`
- **Body:**
```json
{
    "email": "user@example.com",
    "password": "your_password"
}
```

#### Create User
- **POST** `/api/createuser`
- **Body:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "your_password",
    "confirm_password": "your_password",
    "role": "client"  // or "attorney"
}
```

#### Create Admin User
- **POST** `/api/createadmin`
- **Headers:** `Authorization: Bearer <token>`
- **Body:**
```json
{
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com",
    "password": "admin_password",
    "confirm_password": "admin_password"
}
```

### User Management

#### Get User List
- **GET** `/api/listusers`
- **Headers:** `Authorization: Bearer <token>`
- **Query Parameters:**
  - `role`: Filter by user role (admin, client, attorney)

#### Get User Details
- **GET** `/api/getuserbyid/:id`
- **Headers:** `Authorization: Bearer <token>`

#### Update User
- **PUT** `/api/getuserbyid/:id`
- **Headers:** `Authorization: Bearer <token>`
- **Body:**
```json
{
    "first_name": "Updated",
    "last_name": "Name",
    "image": "new_image_url"
}
```

#### Delete User
- **DELETE** `/api/getuserbyid/:id`
- **Headers:** `Authorization: Bearer <token>`

### OTP Management

#### Verify OTP
- **POST** `/api/verifyotp`
- **Body:**
```json
{
    "email": "user@example.com",
    "otp": "123456"
}
```

#### Request New OTP
- **POST** `/api/createotp`
- **Body:**
```json
{
    "email": "user@example.com"
}
```

## Project Structure

```
main-backend/
├── backend/
│   ├── legalUser/
│   │   ├── API/
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py
│   │   │   └── authentication.py
│   │   ├── models.py
│   │   ├── admin.py
│   │   └── apps.py
│   ├── legal/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── manage.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/main-backend](https://github.com/yourusername/main-backend)
