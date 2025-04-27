import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import json
import os

# Inisialisasi Faker
fake = Faker('id_ID')
random.seed(42)
np.random.seed(42)
fake.seed_instance(42)

# 1. USER Table
def generate_dummy_users(n=1000):
    users = []
    used_ids = set()

    for _ in range(n):
        while True:
            user_id = fake.unique.random_int(min=1000, max=9999)
            if user_id not in used_ids:
                used_ids.add(user_id)
                break

        registration_date = fake.date_time_this_decade()
        last_login = fake.date_time_between(start_date=registration_date, end_date=datetime.now())

        user = {
            "user_id": user_id,
            "username": fake.user_name(),
            "email": fake.email(),
            "password_hash": fake.sha256(),
            "phone_number": fake.phone_number(),
            "registration_date": registration_date,
            "is_active": random.choice([0, 1]),
            "last_login": last_login,
            "profile_picture": fake.image_url(),
            "is_verified": random.choice([0, 1]),
            "wallet_balance": round(random.uniform(0, 10000), 2)
        }
        users.append(user)

    return pd.DataFrame(users)

# 2. SELLER Table
def generate_sellers(users_df, percentage=0.4):
    num_sellers = int(len(users_df) * percentage)
    seller_user_ids = random.sample(users_df['user_id'].tolist(), num_sellers)

    sellers = []
    for i, user_id in enumerate(seller_user_ids, 1):
        user = users_df[users_df['user_id'] == user_id].iloc[0]
        registration_date = user['registration_date']
        joined_date = registration_date + timedelta(days=random.randint(1, 30))

        sellers.append({
            "seller_id": i,
            "user_id": user_id,
            "shop_name": fake.company(),
            "description": fake.paragraph(),
            "shop_banner": fake.image_url() if random.random() > 0.4 else '',
            "shop_logo": fake.image_url() if random.random() > 0.3 else '',
            "joined_date": joined_date,
            "is_official": random.choice([0, 1]),
            "rating": round(random.uniform(3.0, 5.0), 1),
            "total_products": random.randint(5, 150),
            "followers_count": random.randint(0, 5000)
        })
    return pd.DataFrame(sellers)

# 3. BUYER Table
def generate_buyers(users_df):
    buyers = []
    for i, user in users_df.iterrows():
        has_purchased = random.random() > 0.2
        orders_count = random.randint(0, 20) if has_purchased else 0
        last_purchase = fake.date_time_between(start_date=user['registration_date'], end_date='now') if has_purchased else pd.Timestamp('1970-01-01')

        buyers.append({
            "buyer_id": i + 1,
            "user_id": user['user_id'],
            "total_spent": round(random.uniform(0, 10000000), 2) if orders_count > 0 else 0,
            "orders_count": orders_count,
            "last_purchase": last_purchase
        })
    return pd.DataFrame(buyers)

# 4. ADDRESS Table
def generate_addresses(users_df):
    addresses = []
    address_id = 1

    for _, user in users_df.iterrows():
        num_addresses = random.randint(1, 3)

        for j in range(num_addresses):
            address_line2 = f"RT {random.randint(1, 20)}/RW {random.randint(1, 10)}, {fake.street_name()}" if random.random() > 0.5 else ''

            addresses.append({
                "address_id": address_id,
                "user_id": user['user_id'],
                "recipient_name": fake.name(),
                "phone_number": fake.phone_number(),
                "address_line1": fake.street_address(),
                "address_line2": address_line2,
                "city": fake.city(),
                "postal_code": fake.postcode(),
                "province": fake.state(),
                "country": "Indonesia",
                "is_default": 1 if j == 0 else 0,
                "label": random.choice(['Rumah', 'Kantor', 'Kost', 'Apartemen', 'Alamat Pengiriman'])
            })
            address_id += 1

    return pd.DataFrame(addresses)

# 5. PRODUCT_CATEGORY Table
def generate_product_categories():
    categories = [
        {'category_id': 1, 'parent_category_id': 0, 'category_name': 'Fashion', 'level': 1, 'display_order': 1},
        {'category_id': 2, 'parent_category_id': 0, 'category_name': 'Elektronik', 'level': 1, 'display_order': 2},
        {'category_id': 3, 'parent_category_id': 0, 'category_name': 'Kesehatan & Kecantikan', 'level': 1, 'display_order': 3},
        {'category_id': 4, 'parent_category_id': 0, 'category_name': 'Rumah Tangga', 'level': 1, 'display_order': 4},
        {'category_id': 5, 'parent_category_id': 0, 'category_name': 'Olahraga & Hobi', 'level': 1, 'display_order': 5},
        {'category_id': 6, 'parent_category_id': 1, 'category_name': 'Pakaian Pria', 'level': 2, 'display_order': 1},
        {'category_id': 7, 'parent_category_id': 1, 'category_name': 'Pakaian Wanita', 'level': 2, 'display_order': 2},
        {'category_id': 8, 'parent_category_id': 1, 'category_name': 'Tas & Dompet', 'level': 2, 'display_order': 3},
        {'category_id': 9, 'parent_category_id': 1, 'category_name': 'Sepatu', 'level': 2, 'display_order': 4},
        {'category_id': 10, 'parent_category_id': 1, 'category_name': 'Aksesoris', 'level': 2, 'display_order': 5},
        {'category_id': 11, 'parent_category_id': 2, 'category_name': 'Handphone & Tablet', 'level': 2, 'display_order': 1},
        {'category_id': 12, 'parent_category_id': 2, 'category_name': 'Laptop & Komputer', 'level': 2, 'display_order': 2},
        {'category_id': 13, 'parent_category_id': 2, 'category_name': 'Audio & Video', 'level': 2, 'display_order': 3},
        {'category_id': 14, 'parent_category_id': 2, 'category_name': 'Kamera', 'level': 2, 'display_order': 4},
        {'category_id': 15, 'parent_category_id': 2, 'category_name': 'Aksesoris Elektronik', 'level': 2, 'display_order': 5},
        {'category_id': 16, 'parent_category_id': 3, 'category_name': 'Makeup', 'level': 2, 'display_order': 1},
        {'category_id': 17, 'parent_category_id': 3, 'category_name': 'Perawatan Kulit', 'level': 2, 'display_order': 2},
        {'category_id': 18, 'parent_category_id': 3, 'category_name': 'Perawatan Rambut', 'level': 2, 'display_order': 3},
        {'category_id': 19, 'parent_category_id': 3, 'category_name': 'Perawatan Tubuh', 'level': 2, 'display_order': 4},
        {'category_id': 20, 'parent_category_id': 3, 'category_name': 'Suplemen & Vitamin', 'level': 2, 'display_order': 5},
        {'category_id': 31, 'parent_category_id': 6, 'category_name': 'Kemeja Pria', 'level': 3, 'display_order': 1},
        {'category_id': 32, 'parent_category_id': 6, 'category_name': 'Kaos Pria', 'level': 3, 'display_order': 2},
        {'category_id': 33, 'parent_category_id': 6, 'category_name': 'Celana Pria', 'level': 3, 'display_order': 3},
        {'category_id': 34, 'parent_category_id': 6, 'category_name': 'Jaket Pria', 'level': 3, 'display_order': 4},
        {'category_id': 35, 'parent_category_id': 7, 'category_name': 'Atasan Wanita', 'level': 3, 'display_order': 1},
        {'category_id': 36, 'parent_category_id': 7, 'category_name': 'Bawahan Wanita', 'level': 3, 'display_order': 2},
        {'category_id': 37, 'parent_category_id': 7, 'category_name': 'Dress', 'level': 3, 'display_order': 3},
    ]

    for category in categories:
        category['description'] = f"Kategori untuk produk {category['category_name']}"
        category['icon_url'] = f"https://ecommerce.com/categories/icons/{category['category_id']}.png"

    return pd.DataFrame(categories)

# 6. PRODUCT Table
def generate_products(sellers_df, categories_df):
    products = []
    product_id = 1

    parent_categories = categories_df[categories_df['parent_category_id'].notna()]['parent_category_id'].unique().tolist()
    leaf_categories = categories_df[~categories_df['category_id'].isin(parent_categories)]['category_id'].tolist()

    for _, seller in sellers_df.iterrows():
        num_products = min(random.randint(3, 10), seller['total_products'])

        for _ in range(num_products):
            category_id = random.choice(leaf_categories)
            created_at = fake.date_time_between(start_date=seller['joined_date'], end_date='now')
            updated_at = fake.date_time_between(start_date=created_at, end_date='now')

            min_price = round(random.uniform(10000, 5000000), -3)
            max_price = min_price * random.uniform(1, 1.5)

            products.append({
                "product_id": product_id,
                "seller_id": seller['seller_id'],
                "category_id": category_id,
                "product_name": fake.catch_phrase(),
                "description": fake.paragraph(),
                "long_description": fake.text(max_nb_chars=1000),
                "min_price": min_price,
                "max_price": max_price,
                "seller_sku": fake.bothify(text='???-#####'),
                "total_stock": random.randint(0, 1000),
                "rating": round(random.uniform(1.0, 5.0), 1) if random.random() > 0.2 else 0,
                "sold_count": random.randint(0, 500),
                "views_count": random.randint(10, 5000),
                "is_active": random.choice([0, 1]),
                "created_at": created_at,
                "updated_at": updated_at
            })
            product_id += 1

    return pd.DataFrame(products)

# 7. PRODUCT_VARIANT Table
def generate_product_variants(products_df):
    variants = []
    variant_id = 1

    for _, product in products_df.iterrows():
        num_variants = random.randint(1, 5)

        for v in range(num_variants):
            price_modifier = random.uniform(0.9, 1.1)
            price = round(product['min_price'] * price_modifier, -3)

            variant_name = fake.word().capitalize()
            if num_variants > 1:
                variant_name = f"{variant_name} - Variant {v+1}"

            variants.append({
                "variant_id": variant_id,
                "product_id": product['product_id'],
                "variant_name": variant_name,
                "sku": f"{product['seller_sku']}-{v+1}",
                "price": price,
                "stock": random.randint(0, int(product['total_stock'] / num_variants)),
                "image_url": fake.image_url(),
                "is_active": random.choice([0, 1])
            })
            variant_id += 1

    return pd.DataFrame(variants)

# 8. VARIANT_OPTION Table
def generate_variant_options(variants_df):
    options = []
    option_id = 1

    variant_types = {
        'Warna': ['Merah', 'Biru', 'Hitam', 'Putih', 'Abu-abu', 'Coklat', 'Hijau', 'Kuning', 'Pink', 'Ungu'],
        'Ukuran': ['S', 'M', 'L', 'XL', 'XXL', '36', '37', '38', '39', '40', '41', '42', '43'],
        'Kapasitas': ['32GB', '64GB', '128GB', '256GB', '512GB', '1TB'],
        'Tipe': ['Regular', 'Premium', 'Deluxe', 'Limited', 'Special'],
    }

    for _, variant in variants_df.iterrows():
        num_options = random.randint(1, 3)
        option_types = random.sample(list(variant_types.keys()), num_options)

        for option_type in option_types:
            option_value = random.choice(variant_types[option_type])

            options.append({
                "option_id": option_id,
                "variant_id": variant['variant_id'],
                "option_type": option_type,
                "option_value": option_value
            })
            option_id += 1

    return pd.DataFrame(options)

# 9. PRODUCT_IMAGE Table
def generate_product_images(products_df):
    images = []
    image_id = 1

    for _, product in products_df.iterrows():
        num_images = random.randint(1, 5)

        for i in range(num_images):
            is_primary = 1 if i == 0 else 0

            images.append({
                "image_id": image_id,
                "product_id": product['product_id'],
                "image_url": fake.image_url(),
                "is_primary": is_primary,
                "display_order": i + 1
            })
            image_id += 1

    return pd.DataFrame(images)

# 10. CART Table
def generate_carts(users_df):
    carts = []

    for _, user in users_df.iterrows():
        carts.append({
            "cart_id": len(carts) + 1,
            "user_id": user['user_id'],
            "last_updated": fake.date_time_between(start_date=user['registration_date'], end_date='now')
        })

    return pd.DataFrame(carts)

# 11. CART_ITEM Table
def generate_cart_items(carts_df, variants_df, active_cart_percentage=0.7):
    cart_items = []
    cart_item_id = 1

    active_cart_ids = random.sample(carts_df['cart_id'].tolist(),
                                    int(len(carts_df) * active_cart_percentage))

    for cart_id in active_cart_ids:
        num_items = random.randint(1, 5)
        cart = carts_df[carts_df['cart_id'] == cart_id].iloc[0]

        sample_variants = variants_df.sample(num_items) if len(variants_df) >= num_items else variants_df

        for _, variant in sample_variants.iterrows():
            added_at = fake.date_time_between(start_date='-30d', end_date='now')

            cart_items.append({
                "cart_item_id": cart_item_id,
                "cart_id": cart_id,
                "variant_id": variant['variant_id'],
                "quantity": random.randint(1, 5),
                "price_at_addition": variant['price'],
                "added_at": added_at,
                "is_selected": random.choice([0, 1])
            })
            cart_item_id += 1

    return pd.DataFrame(cart_items)

# 12. ORDER Table
def generate_orders(buyers_df):
    orders = []
    order_id = 1

    for _, buyer in buyers_df.iterrows():
        if buyer['orders_count'] > 0:
            for _ in range(int(buyer['orders_count'])):
                order_date = fake.date_time_between(start_date='-2y', end_date='now')

                subtotal = round(random.uniform(50000, 2000000), -3)
                shipping_fee = round(random.uniform(10000, 50000), -3)
                platform_fee = round(subtotal * 0.05, -3)
                tax = round(subtotal * 0.11, -3)

                discount = 0
                if random.random() < 0.3:
                    discount = round(subtotal * random.uniform(0.05, 0.2), -3)

                total_amount = subtotal + shipping_fee + platform_fee + tax - discount

                payment_method = random.choice(['Credit Card', 'Bank Transfer', 'E-Wallet', 'COD', 'QRIS'])
                payment_status = random.choice(['Pending', 'Paid', 'Failed', 'Refunded'])

                payment_date = order_date
                if payment_status == 'Paid':
                    payment_date = order_date + timedelta(hours=random.randint(1, 24))
                elif payment_status == 'Failed':
                    payment_date = order_date + timedelta(hours=random.randint(24, 72))
                elif payment_status == 'Refunded':
                    payment_date = order_date + timedelta(days=random.randint(1, 7))

                orders.append({
                    "order_id": order_id,
                    "buyer_id": buyer['buyer_id'],
                    "order_number": fake.bothify(text='ORD-########'),
                    "order_date": order_date,
                    "subtotal": subtotal,
                    "shipping_fee": shipping_fee,
                    "platform_fee": platform_fee,
                    "tax": tax,
                    "discount": discount,
                    "total_amount": total_amount,
                    "payment_method": payment_method,
                    "payment_status": payment_status,
                    "payment_date": payment_date if payment_status != 'Pending' else pd.Timestamp('1970-01-01')
                })
                order_id += 1

    return pd.DataFrame(orders)

# 13. ORDER_ITEM Table
def generate_order_items(orders_df, sellers_df, variants_df):
    order_items = []
    order_item_id = 1

    order_status_flow = ['Processing', 'Shipped', 'Delivered', 'Completed', 'Cancelled', 'Returned']

    for _, order in orders_df.iterrows():
        if order['payment_status'] == 'Failed':
            continue

        num_items = random.randint(1, 5)
        seller_ids = sellers_df.sample(min(num_items, len(sellers_df)))['seller_id'].tolist()

        for i in range(num_items):
            seller_id = seller_ids[i % len(seller_ids)]
            variant = variants_df.sample().iloc[0]

            quantity = random.randint(1, 3)
            unit_price = variant['price']
            subtotal = unit_price * quantity

            if order['payment_status'] == 'Pending':
                order_status = 'Processing'
            elif order['payment_status'] == 'Refunded':
                order_status = random.choice(['Returned', 'Cancelled'])
            else:
                order_status = random.choices(
                    order_status_flow,
                    weights=[0.1, 0.2, 0.3, 0.3, 0.05, 0.05],
                    k=1
                )[0]

            status_updated = order['order_date']
            if order_status == 'Shipped':
                status_updated = order['order_date'] + timedelta(days=random.randint(1, 2))
            elif order_status == 'Delivered':
                status_updated = order['order_date'] + timedelta(days=random.randint(3, 7))
            elif order_status == 'Completed':
                status_updated = order['order_date'] + timedelta(days=random.randint(8, 14))

            tracking_number = fake.bothify(text='TRK-########') if order_status in ['Shipped', 'Delivered', 'Completed'] else ''
            shipping_method = random.choice(['Regular', 'Express', 'Same Day', 'Economy']) if order_status in ['Shipped', 'Delivered', 'Completed'] else ''
            estimated_delivery = order['order_date'] + timedelta(days=random.randint(3, 10)) if order_status in ['Shipped', 'Delivered', 'Completed'] else pd.Timestamp('1970-01-01')

            order_items.append({
                "order_item_id": order_item_id,
                "order_id": order['order_id'],
                "seller_id": seller_id,
                "variant_id": variant['variant_id'],
                "quantity": quantity,
                "unit_price": unit_price,
                "subtotal": subtotal,
                "order_status": order_status,
                "status_updated": status_updated,
                "tracking_number": tracking_number,
                "shipping_method": shipping_method,
                "estimated_delivery": estimated_delivery
            })
            order_item_id += 1

    return pd.DataFrame(order_items)

# 14. VOUCHER Table
def generate_vouchers(sellers_df):
    vouchers = []
    voucher_id = 1

    for _, seller in sellers_df.iterrows():
        num_vouchers = random.randint(0, 5)

        for _ in range(num_vouchers):
            is_percentage = random.choice([0, 1])

            if is_percentage:
                discount_amount = random.randint(5, 50)
                minimum_purchase = round(random.uniform(50000, 200000), -3)
            else:
                discount_amount = round(random.uniform(10000, 100000), -3)
                minimum_purchase = round(discount_amount * random.uniform(2, 5), -3)

            is_free_shipping = random.choice([0, 1])
            start_date_v = fake.date_between(start_date='-1y', end_date='+3m')
            end_date_v = fake.date_between(start_date=start_date_v, end_date=start_date_v + timedelta(days=90))

            vouchers.append({
                "voucher_id": voucher_id,
                "seller_id": seller['seller_id'],
                "code": fake.bothify(text='???###').upper(),
                "description": fake.sentence(),
                "discount_amount": discount_amount,
                "minimum_purchase": minimum_purchase,
                "is_percentage": is_percentage,
                "is_free_shipping": is_free_shipping,
                "usage_limit": random.randint(50, 1000),
                "times_used": random.randint(0, 49),
                "start_date": start_date_v,
                "end_date": end_date_v,
                "is_active": random.choice([0, 1])
            })
            voucher_id += 1

    return pd.DataFrame(vouchers)

# 15. USER_VOUCHER Table
def generate_user_vouchers(users_df, vouchers_df):
    user_vouchers = []
    user_voucher_id = 1

    for _, user in users_df.iterrows():
        num_vouchers = random.randint(0, 3)

        if num_vouchers > 0 and len(vouchers_df) > 0:
            sample_vouchers = vouchers_df.sample(min(num_vouchers, len(vouchers_df)))

            for _, voucher in sample_vouchers.iterrows():
                is_used = random.choice([0, 1])
                used_at = fake.date_time_between(start_date='-30d', end_date='now') if is_used else pd.Timestamp('1970-01-01')
                expires_at = fake.date_time_between(start_date='now', end_date='+30d')

                user_vouchers.append({
                    "user_voucher_id": user_voucher_id,
                    "user_id": user['user_id'],
                    "voucher_id": voucher['voucher_id'],
                    "is_used": is_used,
                    "used_at": used_at,
                    "expires_at": expires_at
                })
                user_voucher_id += 1

    return pd.DataFrame(user_vouchers)

# 16. WISHLIST Table
def generate_wishlists(users_df):
    wishlists = []
    wishlist_id = 1

    for _, user in users_df.iterrows():
        num_wishlists = random.randint(0, 2)

        for i in range(num_wishlists):
            created_at = fake.date_time_between(start_date=user['registration_date'], end_date='now')

            name = "Wishlist Saya"
            if i > 0:
                name = f"Wishlist {fake.word().capitalize()}"

            wishlists.append({
                "wishlist_id": wishlist_id,
                "user_id": user['user_id'],
                "name": name,
                "is_public": random.choice([0, 1]),
                "created_at": created_at
            })
            wishlist_id += 1

    return pd.DataFrame(wishlists)

# 17. WISHLIST_ITEM Table
def generate_wishlist_items(wishlists_df, products_df):
    wishlist_items = []
    wishlist_item_id = 1

    for _, wishlist in wishlists_df.iterrows():
        num_items = random.randint(1, 10)
        sample_products = products_df.sample(min(num_items, len(products_df)))

        for _, product in sample_products.iterrows():
            added_at = fake.date_time_between(start_date=wishlist['created_at'], end_date='now')

            wishlist_items.append({
                "wishlist_item_id": wishlist_item_id,
                "wishlist_id": wishlist['wishlist_id'],
                "product_id": product['product_id'],
                "added_at": added_at
            })
            wishlist_item_id += 1

    return pd.DataFrame(wishlist_items)

# 18. NOTIFICATION Table
def generate_notifications(users_df):
    notifications = []
    notification_id = 1

    notification_types = ['order', 'promo', 'payment', 'shipping', 'system']

    for _, user in users_df.iterrows():
        num_notifications = random.randint(0, 15)

        for _ in range(num_notifications):
            notification_type = random.choice(notification_types)
            created_at = fake.date_time_between(start_date=user['registration_date'], end_date='now')
            is_read = random.choice([0, 1])

            title_prefix = {
                'order': 'Pesanan Anda',
                'promo': 'Promo Spesial',
                'payment': 'Pembayaran',
                'shipping': 'Pengiriman',
                'system': 'Pemberitahuan Sistem'
            }

            title = f"{title_prefix[notification_type]} {fake.word().capitalize()}"

            notifications.append({
                "notification_id": notification_id,
                "user_id": user['user_id'],
                "title": title,
                "message": fake.sentence(),
                "notification_type": notification_type,
                "reference_id": fake.bothify(text='REF-#####'),
                "is_read": is_read,
                "created_at": created_at
            })
            notification_id += 1

    return pd.DataFrame(notifications)

# 19. CHAT Table
def generate_chats(users_df, limit=500):
    chats = []
    chat_id = 1

    for _ in range(limit):
        sender_user = users_df.sample().iloc[0]
        receiver_user = users_df[users_df['user_id'] != sender_user['user_id']].sample().iloc[0]

        sent_at = fake.date_time_between(start_date='-6m', end_date='now')

        message_types = ['text', 'image', 'product']
        message_type = random.choices(message_types, weights=[0.8, 0.15, 0.05], k=1)[0]

        if message_type == 'text':
            message = fake.sentence()
        elif message_type == 'image':
            message = fake.image_url()
        else:
            message = f"PRODUCT:{random.randint(1, 100)}"

        chats.append({
            "chat_id": chat_id,
            "sender_id": sender_user['user_id'],
            "receiver_id": receiver_user['user_id'],
            "message": message,
            "message_type": message_type,
            "is_read": random.choice([0, 1]),
            "sent_at": sent_at
        })
        chat_id += 1

    return pd.DataFrame(chats)

# 20. PROMOTION Table
def generate_promotions(limit=20):
    promotions = []
    promotion_id = 1

    target_types = ['category', 'product', 'seller', 'all']

    for _ in range(limit):
        target_type = random.choice(target_types)

        if target_type == 'category':
            reference_id = str(random.randint(1, 20))
        elif target_type == 'product':
            reference_id = str(random.randint(1, 100))
        elif target_type == 'seller':
            reference_id = str(random.randint(1, 20))
        else:
            reference_id = 'ALL'

        start_date_p = fake.date_between(start_date='-2m', end_date='+1m')
        end_date_p = fake.date_between(start_date=start_date_p, end_date=start_date_p + timedelta(days=30))

        promotions.append({
            "promotion_id": promotion_id,
            "title": f"Promo {fake.word().capitalize()}",
            "description": fake.paragraph(),
            "banner_url": fake.image_url(),
            "start_date": start_date_p,
            "end_date": end_date_p,
            "target_type": target_type,
            "reference_id": reference_id,
            "is_active": random.choice([0, 1])
        })
        promotion_id += 1

    return pd.DataFrame(promotions)

# 21. PRODUCT_REVIEW Table
def generate_product_reviews(products_df, order_items_df, users_df, product_variants_df):
    reviews = []
    review_id = 1

    # Filter order_items yang statusnya Delivered atau Completed
    completed_order_items = order_items_df[order_items_df['order_status'].isin(['Delivered', 'Completed'])]

    # Jika tidak ada order_items yang selesai, kembalikan DataFrame kosong
    if completed_order_items.empty:
        print("Tidak ada order_items dengan status Delivered atau Completed untuk membuat review.")
        return pd.DataFrame(reviews)

    # Gabungkan order_items dengan product_variants untuk mendapatkan product_id
    completed_order_items = completed_order_items.merge(
        product_variants_df[['variant_id', 'product_id']],
        on='variant_id',
        how='left'
    )

    # Pastikan semua variant_id memiliki product_id yang sesuai
    if completed_order_items['product_id'].isna().any():
        print("Warning: Ada variant_id di order_items yang tidak ditemukan di product_variants.")
        completed_order_items = completed_order_items.dropna(subset=['product_id'])

    # Pastikan semua product_id ada di products_df
    completed_order_items = completed_order_items[completed_order_items['product_id'].isin(products_df['product_id'])]

    if completed_order_items.empty:
        print("Tidak ada order_items yang cocok dengan product_id di products untuk membuat review.")
        return pd.DataFrame(reviews)

    # Iterasi berdasarkan order_items yang valid
    for _, order_item in completed_order_items.iterrows():
        # Tentukan apakah akan membuat review untuk order_item ini (misalnya, 50% kemungkinan)
        if random.random() < 0.5:
            user_id = random.choice(users_df['user_id'].tolist())

            review_date = fake.date_time_between(
                start_date=order_item['status_updated'],
                end_date=order_item['status_updated'] + timedelta(days=14)
            )

            media_urls = []
            if random.random() < 0.3:
                num_media = random.randint(1, 3)
                for i in range(num_media):
                    media_urls.append(f"https://ecommerce.com/reviews/{review_id}/media/{i+1}.jpg")

            reviews.append({
                "review_id": review_id,
                "product_id": int(order_item['product_id']),  # Pastikan tipe data integer
                "user_id": user_id,
                "order_item_id": order_item['order_item_id'],
                "rating": random.randint(1, 5),
                "comment": fake.paragraph(),
                "review_date": review_date,
                "media_urls": json.dumps(media_urls) if media_urls else '[]',
                "helpful_votes": random.randint(0, 50)
            })
            review_id += 1

    return pd.DataFrame(reviews)

# Fungsi untuk menghasilkan semua data
def generate_all_data(num_users=50):
    all_tables = {}

    print("BAGIAN 1: MENGHASILKAN 10 TABEL PERTAMA")
    print("---------------------------------------")

    print("Generating Users...")
    users_df = generate_dummy_users(num_users)
    all_tables['users'] = users_df

    print("Generating Sellers...")
    sellers_df = generate_sellers(users_df)
    all_tables['sellers'] = sellers_df

    print("Generating Buyers...")
    buyers_df = generate_buyers(users_df)
    all_tables['buyers'] = buyers_df

    print("Generating Addresses...")
    addresses_df = generate_addresses(users_df)
    all_tables['addresses'] = addresses_df

    print("Generating Product Categories...")
    categories_df = generate_product_categories()
    all_tables['product_categories'] = categories_df

    print("Generating Products...")
    products_df = generate_products(sellers_df, categories_df)
    all_tables['products'] = products_df

    print("Generating Product Variants...")
    variants_df = generate_product_variants(products_df)
    all_tables['product_variants'] = variants_df

    print("Generating Variant Options...")
    options_df = generate_variant_options(variants_df)
    all_tables['variant_options'] = options_df

    print("Generating Product Images...")
    images_df = generate_product_images(products_df)
    all_tables['product_images'] = images_df

    print("Generating Carts...")
    carts_df = generate_carts(users_df)
    all_tables['carts'] = carts_df

    print("\nBAGIAN 2: MENGHASILKAN 11 TABEL BERIKUTNYA")
    print("------------------------------------------")

    print("Generating Cart Items...")
    cart_items_df = generate_cart_items(carts_df, variants_df)
    all_tables['cart_items'] = cart_items_df

    print("Generating Orders...")
    orders_df = generate_orders(buyers_df)
    all_tables['orders'] = orders_df

    print("Generating Order Items...")
    order_items_df = generate_order_items(orders_df, sellers_df, variants_df)
    all_tables['order_items'] = order_items_df

    print("Generating Vouchers...")
    vouchers_df = generate_vouchers(sellers_df)
    all_tables['vouchers'] = vouchers_df

    print("Generating User Vouchers...")
    user_vouchers_df = generate_user_vouchers(users_df, vouchers_df)
    all_tables['user_vouchers'] = user_vouchers_df

    print("Generating Wishlists...")
    wishlists_df = generate_wishlists(users_df)
    all_tables['wishlists'] = wishlists_df

    print("Generating Wishlist Items...")
    wishlist_items_df = generate_wishlist_items(wishlists_df, products_df)
    all_tables['wishlist_items'] = wishlist_items_df

    print("Generating Notifications...")
    notifications_df = generate_notifications(users_df)
    all_tables['notifications'] = notifications_df

    print("Generating Chats...")
    chats_df = generate_chats(users_df, limit=200)
    all_tables['chats'] = chats_df

    print("Generating Promotions...")
    promotions_df = generate_promotions(limit=15)
    all_tables['promotions'] = promotions_df

    print("Generating Product Reviews...")
    reviews_df = generate_product_reviews(products_df, order_items_df, users_df, variants_df)  # Tambahkan variants_df
    all_tables['product_reviews'] = reviews_df

    # Verifikasi integritas foreign key untuk product_reviews
    print("\nMemverifikasi integritas foreign key untuk product_reviews...")
    invalid_product_ids = reviews_df[~reviews_df['product_id'].isin(products_df['product_id'])]['product_id'].unique()
    if len(invalid_product_ids) > 0:
        print(f"Error: Terdapat product_id di product_reviews yang tidak ada di products: {invalid_product_ids}")
        raise ValueError("Foreign key constraint akan gagal untuk product_reviews karena product_id tidak valid.")
    print("Verifikasi product_reviews: Semua product_id valid.")

    print("\nMemverifikasi tidak ada NaN di semua tabel...")
    for table_name, df in all_tables.items():
        if df.isna().sum().sum() > 0:
            print(f"Error: Tabel {table_name} masih mengandung NaN!")
            print("Detail kolom dengan NaN:")
            print(df.isna().sum())
            raise ValueError(f"Tabel {table_name} mengandung NaN, padahal seharusnya tidak ada!")
        print(f"Tabel {table_name}: Tidak ada NaN.")

    return all_tables

# Fungsi untuk menyimpan data ke file CSV
def save_data_to_csv(data_dict, output_dir="dummy_data/"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    part1_dir = os.path.join(output_dir, "part1/")
    part2_dir = os.path.join(output_dir, "part2/")

    if not os.path.exists(part1_dir):
        os.makedirs(part1_dir)

    if not os.path.exists(part2_dir):
        os.makedirs(part2_dir)

    part1_tables = ['users', 'sellers', 'buyers', 'addresses', 'product_categories',
                   'products', 'product_variants', 'variant_options', 'product_images', 'carts']

    part2_tables = ['cart_items', 'orders', 'order_items', 'vouchers', 'user_vouchers',
                   'wishlists', 'wishlist_items', 'notifications', 'chats', 'promotions', 'product_reviews']

    print("\nMemverifikasi data sebelum menyimpan...")
    for table_name, df in data_dict.items():
        if df.isna().sum().sum() > 0:
            print(f"Error: Tabel {table_name} masih mengandung NaN!")
            print("Detail kolom dengan NaN:")
            print(df.isna().sum())
            raise ValueError(f"Tabel {table_name} mengandung NaN, padahal seharusnya tidak ada!")

    print("\nMenyimpan data bagian 1...")
    for table_name in part1_tables:
        if table_name in data_dict:
            file_path = os.path.join(part1_dir, f"{table_name}.csv")
            data_dict[table_name].to_csv(file_path, index=False)
            print(f"✓ Data {table_name} disimpan ke {file_path}")

    print("\nMenyimpan data bagian 2...")
    for table_name in part2_tables:
        if table_name in data_dict:
            file_path = os.path.join(part2_dir, f"{table_name}.csv")
            data_dict[table_name].to_csv(file_path, index=False)
            print(f"✓ Data {table_name} disimpan ke {file_path}")

    print("\nSemua data berhasil disimpan!")

# Main Execution
if __name__ == "__main__":
    print("==============================================")
    print(" GENERATOR DATA DUMMY E-COMMERCE ")
    print("==============================================")

    num_users = int(input("Masukkan jumlah user yang ingin dibuat (default 50): ") or "50")

    print(f"\nMembuat data dummy untuk {num_users} pengguna...")

    all_data = generate_all_data(num_users)

    print("\n=== STATISTIK DATA YANG DIHASILKAN ===")
    for name, df in all_data.items():
        print(f"{name.capitalize()}: {len(df)} baris")

    save_data = input("\nApakah Anda ingin menyimpan data ke CSV? (y/n): ").lower().strip() == 'y'

    if save_data:
        output_dir = input("Masukkan direktori output (default 'dummy_data/'): ") or "dummy_data/"
        save_data_to_csv(all_data, output_dir)

    print("\nSelesai!")
