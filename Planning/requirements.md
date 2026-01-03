# eCommerce System Requirements

## 1. User Types and Roles

### 1.1 Vendors
- **Registration & Authentication**: Vendors can register and log in to the system
- **Store Management**:
  - Create new stores
  - View all their stores
  - Edit store information
  - Delete stores
- **Product Management**:
  - Add products to their stores
  - View products in their stores
  - Edit product information
  - Remove products from stores

### 1.2 Buyers
- **Registration & Authentication**: Buyers can register and log in to the system
- **Product Browsing**: View products from different stores
- **Shopping Cart**:
  - Add products to cart
  - View cart contents
  - Update cart quantities
  - Remove items from cart
  - Cart persists using sessions
- **Checkout Process**:
  - Complete purchase
  - Receive email invoice
  - Cart cleared after successful checkout
- **Reviews**:
  - Leave reviews for products
  - Reviews can be verified (if product was purchased) or unverified (if not purchased)

## 2. System Features

### 2.1 Authentication & Authorization
- User registration (Vendor or Buyer)
- User login/logout
- Password reset via email with expiring tokens
- Role-based access control (vendors can only manage their stores/products, buyers can only access buyer features)

### 2.2 Session Management
- Shopping cart stored in session
- User session management
- Secure session handling

### 2.3 Email Functionality
- Send invoice emails after checkout
- Send password reset emails with secure tokens

### 2.4 Review System
- Verified reviews: Reviews from users who purchased the product
- Unverified reviews: Reviews from users who haven't purchased the product
- Display review status clearly

## 3. Technical Requirements

### 3.1 Database
- Use MariaDB or another relational database
- Proper database migrations
- Data integrity and relationships

### 3.2 Security
- Password hashing
- CSRF protection
- SQL injection prevention (Django ORM)
- XSS protection
- Secure token generation for password reset
- Token expiration for password reset

### 3.3 User Interface
- Responsive design
- Intuitive navigation
- Clear separation between vendor and buyer interfaces
- User-friendly forms and error messages

## 4. Data Models

### 4.1 User Models
- Custom User model extending Django's AbstractUser
- User type field (Vendor/Buyer)

### 4.2 Store Model
- Store name, description
- Vendor (foreign key)
- Created/updated timestamps

### 4.3 Product Model
- Product name, description, price
- Store (foreign key)
- Stock quantity
- Created/updated timestamps

### 4.4 Cart Model (Session-based)
- Products and quantities
- User session tracking

### 4.5 Order Model
- User (buyer)
- Order items
- Total amount
- Order date
- Invoice sent status

### 4.6 Review Model
- Product (foreign key)
- User (buyer)
- Rating, comment
- Verified status (based on purchase history)
- Created timestamp

### 4.7 Password Reset Token Model
- User
- Token
- Expiration timestamp
- Used status





