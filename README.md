# Vendor Management System

The Vendor Management System is a Django-based web application designed to handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Installation and Setup

1. Clone the Repository: 
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd vendor
   ```

3. **Create a Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   ```

4. **Activate the Virtual Environment**:
   ```bash
   # On Windows
   venv\Scripts\activate
   # On macOS and Linux
   source venv/bin/activate
   ```

5. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

## Running the Application

1. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the Application**:
   Open postman api testing tool and import the json file from the repo and run the apis.

## API Endpoints

### Vendor Profile Management
- `POST http://localhost:8000/main/api/vendors/`: Create a new vendor.
- `GET http://localhost:8000/main/api/vendors/`: List all vendors.
- `GET http://localhost:8000/main/api/vendors/{vendor_id}/`: Retrieve details of a specific vendor.
- `PUT http://localhost:8000/main/api/vendors/{vendor_id}/`: Update a vendor's details.
- `DELETE http://localhost:8000/main/api/vendors/{vendor_id}/`: Delete a vendor.

### Purchase Order Tracking
- `POST http://localhost:8000/main/api/purchase_orders/`: Create a purchase order.
- `GET http://localhost:8000/main/api/purchase_orders/`: List all purchase orders.
- `GET http://localhost:8000/main/api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order.
- `PUT http://localhost:8000/main/api/purchase_orders/{po_id}/`: Update a purchase order.
- `DELETE http://localhost:8000/main/api/purchase_orders/{po_id}/`: Delete a purchase order.

### Vendor Performance Evaluation(Django Signal is implemented)
- `GET http://localhost:8000/main/api/vendors/{vendor_id}/performance
- `POST http://localhost:8000/main/api/purchase_orders/{po_id}/acknowledge
```markdown
```

## Authentication

Token-based authentication is used to secure the API endpoints. To obtain a token, send a POST request to `http://localhost:8000/api-token-auth/` with valid credentials (username and password). Include the token in the `Authorization` header of subsequent requests to authenticate.
{"username":"manaf","password":"manaf"}  - USE THIS CREDENTIALS TO GET TOKEN

## Additional Details

- Ensure to follow RESTful principles when interacting with the APIs.
- Comprehensive data validations are implemented for models.
- Django ORM is utilized for database interactions.
- API endpoints are secured with token-based authentication.
- PEP 8 style guidelines are followed for Python code.
- API documentation is provided within this README.

Feel free to customize this README file further based on your project's specific requirements and additional information you want to provide to users.
```
