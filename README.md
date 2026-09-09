# Aether Jewels — Celestial Haute Joaillerie E-Commerce Platform

**Aether Jewels** is a client-ready, production-grade Django e-commerce platform designed for a celestial-inspired luxury fine jewellery house in India. Built with deep obsidian aesthetics (`#08080A`), champagne gold accents (`#D4AF37`), Google Fonts (*Playfair Display*, *Cormorant Garamond*, *Plus Jakarta Sans*), Indian Rupee (₹) currency localization, and full authentication & vault order management.

---

## Key Features

### 1. User Authentication & VIP Portal
- **User Registration & Login/Logout**: Secure session authentication with validation for 10-digit Indian phone numbers and email uniqueness.
- **Sovereign Client Portal**: VIP tier indicators (*Member, Silver Astral, Gold Celestial, Solitaire Platinum VIP*), order history tracking, and vault delivery address management.
- **Login-Guarded Checkout**: Protects high-value orders by requiring authentication before order authorization.

### 2. Fine Jewellery Catalogue & Gemological Specs
- **6 Celestial Categories**: Celestial Rings, Astral Necklaces, Starlight Earrings, Solar Bracelets, High Solitaires, Zodiac Talismans.
- **Search & Filtering**: Real-time keyword search, category filter, metal karat filter (18K, 22K, 950 Platinum), gemstone filter (Solitaires, Zambian Emeralds, Ceylon Sapphires, Burmese Rubies), price range sorting (Low to High, High to Low, Newest, Rating, Popularity).
- **Product Detail View**: Multi-angle gallery with responsive thumbnail switcher, detailed craftsmanship and gemological spec sheet (karat, weight in grams, diamond clarity/cut, certification), and customer valuation reviews.
- **Indian PIN Code Delivery Estimator**: Live serviceability check for Indian postal codes (Mumbai, Delhi NCR, Bengaluru, Hyderabad, Jaipur, Kolkata, Chennai).

### 3. Shopping Bag & Sovereign Wishlist
- **Session & User Merged Bag**: Automatically merges guest bag items upon user sign-in.
- **Stock Management**: Prevents overselling with live vault stock checks.
- **Privilege Promo System**: Supports discount coupon codes (e.g. `AETHERLIV` for 10% privilege, `CELESTIAL` for ₹10,000 off).
- **Tax Breakdown**: Calculates 3% Fine Jewellery GST compliant with Indian taxation standards.
- **Wishlist**: Real-time AJAX toggle with navbar counter badge and one-click "Move to Bag".

### 4. Sovereign Orders & Invoicing
- **Multi-Step Luxury Checkout**: Validates full name, email, 10-digit phone, 6-digit Indian PIN code, state, payment method (UPI, Metal Card, NetBanking, VIP Insured COD).
- **Order Success Screen**: Generates unique tracking ID (e.g. `AJ-SECURE-XXXXXX`) and order number (`AJ-2026-XXXXX`).
- **Printable Tax Invoice**: Clean, high-resolution printable tax invoice with BIS Hallmarking numbers, GST breakdown, and client details.

### 5. VIP Concierge & Bespoke Commissions
- **Private Boutique Appointment**: Schedule VIP in-boutique viewings at Mumbai Flagship (Bandra), Delhi DLF Emporio, Bengaluru UB City, Jaipur Heritage Salon or Virtual 4K video consultation.
- **Bespoke Design Inquiry**: Submit custom haute joaillerie briefs directly to master goldsmiths.

### 6. Admin Atelier
- **Django Admin Customization**: Branded header and index titles, order item inlines, visual status badges, product thumbnails, and search by SKU / order number / customer phone.

---

## Tech Stack
- **Backend**: Python 3.12, Django 5.1
- **Database**: SQLite3 (easily interchangeable with PostgreSQL / MySQL)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Luxury Design System & Glassmorphism), Bootstrap 5 CDN, Bootstrap Icons
- **Static Assets**: WhiteNoise middleware for seamless static file serving

---

## Quick Start Guide

### 1. Clone or Open the Repository
```bash
cd Aether_jewels_new
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed Luxury Catalogue & Demo Data
Run the custom seed command to populate 6 categories, 16+ sample high jewellery products with specs & images, discount coupons, and demo client accounts:
```bash
python manage.py seed_data
```

### 5. Run the Local Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## Demo Credentials

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin` | `admin123` | Full access to `/admin/` |
| **VIP Demo Client** | `aarav_sharma` | `luxury123` | Solitaire Platinum VIP member with past orders |
| **VIP Demo Client** | `priya_singhania` | `luxury123` | Gold Celestial VIP member |

### Active Promotional Privilege Codes:
- `AETHERLIV` — 10% off on orders above ₹50,000
- `CELESTIAL` — Flat ₹10,000 off on orders above ₹1,00,000
- `ROYALTY15` — 15% off for Solitaire Platinum club orders above ₹2,00,000

---

---

## Project Structure
```
Aether_jewels_new/
├── aether_jewels/              # Django Project Root
│   ├── settings.py             # Settings, apps, context processors, auth config
│   ├── urls.py                 # Root URL router & admin branding
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/               # UserProfile, registration, login, profile edit
│   ├── store/                  # Categories, Products, Reviews, Catalogue, Filters
│   │   └── management/commands/seed_data.py # Custom seeding command
│   ├── cart/                   # Shopping Cart, Wishlist, Coupons, GST breakdown
│   ├── orders/                 # Checkout, Order placement, Printable Invoices
│   └── consultations/          # Private Salon & Bespoke booking
├── static/
│   ├── css/main.css            # Luxury obsidian & champagne gold styling
│   └── js/main.js              # Gallery switcher, PIN code check, AJAX wishlist
├── templates/
│   ├── base.html               # Master layout
│   ├── includes/               # Navbar, footer, messages
│   ├── store/                  # home, product_list, product_detail
│   ├── cart/                   # cart_detail, wishlist
│   ├── orders/                 # checkout, order_success, order_detail, order_invoice
│   ├── accounts/               # login, register, profile, edit_profile
│   ├── consultations/          # book, bespoke, success
│   └── pages/                  # about, contact, faq
├── requirements.txt
├── README.md
└── manage.py
```
