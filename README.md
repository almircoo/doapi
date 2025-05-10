# Restaurant Supply Management API

A Django REST Framework API for managing restaurant and providers, with JWT authentication, Resend for email validation, and Cloudinary for image uploads.

## Features

- JWT Authentication
- Email verification with Resend
- Image uploads with Cloudinary
- Complete restaurant and provider management system
- Role-based access control

## Setup

1. Clone the repository
2. Create a virtual environment:
   \`\`\`
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`
3. Install dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`
4. Copy `.env.example` to `.env` and fill in your environment variables
5. Run migrations:
   \`\`\`
   python manage.py makemigrations
   python manage.py migrate
   \`\`\`
6. Create a superuser:
   \`\`\`
   python manage.py createsuperuser
   \`\`\`
7. Run the development server:
   \`\`\`
   python manage.py runserver
   \`\`\`

## API Endpoints

### Authentication
- `POST /api/token/`: Get JWT token
- `POST /api/token/refresh/`: Refresh JWT token

### Registration
- `POST /api/register/restaurant/`: Register a new restaurant
- `POST /api/register/proveedor/`: Register a new provider
- `GET /api/verify-email/<token>/`: Verify email

### Geographic Data
- `GET /api/paises/`: List all countries
- `GET /api/departamentos/`: List all departments
- `GET /api/distritos/`: List all districts

### Users
- `GET /api/usuarios/`: List all users (admin only)
- `GET /api/restaurants/`: List all restaurants
- `GET /api/proveedores/`: List all providers

### Products
- `GET /api/categorias/`: List all categories
- `GET /api/productos/`: List all products
- `POST /api/productos/<id>/upload_image/`: Upload product image

### Lists and Carts
- `GET /api/listas/`: List all lists
- `GET /api/lista-items/`: List all list items
- `GET /api/carritos/`: List all carts
- `GET /api/carrito-productos/`: List all cart products

### Orders and Payments
- `GET /api/pagos/`: List all payments
- `GET /api/pedidos/`: List all orders
- `GET /api/pedido-productos/`: List all order products

### Catalogs
- `GET /api/catalogos/`: List all catalogs
- `GET /api/catalogo-productos/`: List all catalog products

### Delivery
- `GET /api/estados-entrega/`: List all delivery statuses
- `GET /api/entregas-pedido/`: List all order deliveries

## License

MIT
