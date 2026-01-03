# Product Image Upload Guide

## Overview
I've added image upload functionality to the eCommerce application. Vendors can now upload product images when creating or editing products.

## What Was Added

### 1. Product Model
- Added `image` field to the `Product` model
- Images are stored in `media/products/` directory
- Images are optional (can be blank/null)

### 2. Product Form
- Added image upload field to the product creation/editing form
- File validation:
  - Maximum file size: 5MB
  - Only image files are accepted
- Shows current image when editing existing products

### 3. Templates Updated
- **Home page**: Displays product images in product cards
- **Product detail page**: Shows large product image
- **Product form**: Shows current image and allows upload
- **Placeholder images**: Uses placeholder service when no image is uploaded

### 4. Media File Handling
- Media files are served during development
- Images are uploaded to `media/products/` directory
- URL pattern: `/media/products/filename.jpg`

## How to Use

### For Vendors:
1. When creating a product, you'll see an "Image" field
2. Click "Choose File" and select an image from your computer
3. Supported formats: JPG, PNG, GIF, etc. (any image format)
4. Maximum file size: 5MB
5. The image will be displayed on the product listing and detail pages

### For Buyers:
- Product images are automatically displayed on:
  - Home page product cards
  - Product detail pages
- If a product doesn't have an image, a placeholder is shown

## Installation Requirements

Make sure you have Pillow installed for image handling:
```bash
pip install Pillow
```

## Database Migration

If you need to add the image column to an existing database, run:
```bash
python manage.py migrate
```

Or if migrations aren't working, you can manually add the column using SQL:
```sql
ALTER TABLE ecommerce_product ADD COLUMN image VARCHAR(100);
```

## Notes

- **I cannot generate images** - You need to provide your own product images
- Images are stored locally in the `media/` directory
- For production, consider using cloud storage (AWS S3, etc.)
- Make sure the `media/` directory exists and is writable
- The `media/` directory should be added to `.gitignore` (already done)

## Image Recommendations

- **Format**: JPG or PNG
- **Size**: Recommended 800x800px or larger (will be resized automatically)
- **Aspect Ratio**: Square images work best for product cards
- **File Size**: Keep under 5MB for faster loading

## Troubleshooting

### Images not displaying?
1. Check that `MEDIA_URL` and `MEDIA_ROOT` are configured in `settings.py`
2. Ensure the `media/` directory exists
3. Check file permissions on the `media/` directory
4. Verify the URL pattern is included in `urls.py`

### Upload errors?
1. Check file size (must be under 5MB)
2. Verify the file is an actual image file
3. Check that Pillow is installed: `pip install Pillow`
4. Ensure the `media/products/` directory exists and is writable

