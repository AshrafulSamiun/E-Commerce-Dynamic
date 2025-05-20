User
-id
-user_name
-role
-name
-email
-mobile_no
-password
-address
-city
-province
-country
-postcode
-created_at
-updated_at
-is_active
-inserted_by
-updated_by

Product
-id
-name
-description
-specification
-sku
-weight
-dimensions
-brand_id
-price
-discount_percentage
-stock
-currency_id
-is_active
-inserted_by
-updated_by
-created_at
-updated_at


Color_size
-id
-product_id
-color_id
-size_id
-price
-discount_percentage
-stock
-is_active
-inserted_by
-updated_by
-created_at
-updated_at

Brand
- id
- name
- slug
- logo_url
- description
- is_active
- inserted_by
- updated_by
- created_at
- updated_at

Color
-id
-name
-is_active
-inserted_by
-updated_by
-created_at
-updated_at

Size
-id
-name
-is_active
-inserted_by
-updated_by
-created_at
-updated_at


Product_image
-id
-product_id
-is_primary 
-color_size_id
-file_path
-is_active
-inserted_by
-updated_by
-created_at
-updated_at

Category
-id
-name
-is_active
-inserted_by
-updated_by
-created_at
-updated_at

Product_categories
-id
-product_id
-category_id
-is_active
-inserted_by
-updated_by
-created_at
-updated_at

Product_review
-id
-user_id
-product_id
-rating
-comment
-is_active
-is_approve
-inserted_by
-updated_by
-created_at
-updated_at

Cart
-id
-user_id
-total_quantity
-total_price
-total_discount
-grand_total
-is_active
-inserted_by
-updated_by
-created_at
-updated_at

Cart_products
-id
-cart_id
-product_id
-color_size_id
-quantity
-price
-discount
-is_active
-inserted_by
-updated_by
-created_at
-updated_at



Order
-id
-user_id
-coupon_id
-mobile_no
-address
-province
-city
-products
-status
-payment_status
-shipping_method
-tracking_number
-total
-tax
-shipping_fee
-discount
-grand_total
-currency_id
-delivery_address
-is_active
-inserted_by
-updated_by
-created_at
-updated_at

Order_products
-id
-order_id
-product_id
-quantity
-price
-discount
-is_active
-inserted_by
-updated_by
-created_at
-updated_at

Coupon
- id
- code
- description
- discount_type (percentage/fixed)
- discount_value
- min_purchase_amount
- max_discount
- start_date
- end_date
- usage_limit
- is_active
- created_at
- updated_at

Notification
- id
- user_id
- title
- message
- type (email, sms, in-app)
- status (sent, read, unread, failed)
- created_at
- read_at

Return
- id
- order_id
- product_id
- user_id
- reason
- status (pending, approved, rejected, refunded)
- refund_amount
- requested_at
- processed_at



Payment
- id
- order_id
- payment_method
- transaction_id
- amount
- currency_id
- status
- payment_date
-payment_gateway_response 
-is_active
-inserted_by
-updated_by
-created_at
-updated_at

Shipping
- id
- order_id
- method
- cost
- tracking_number
- status
- estimated_delivery
-is_active
-inserted_by
-updated_by
-created_at
-updated_at

Currency
- id
- code (USD, EUR, BDT)
- symbol
- exchange_rate
-is_default
-is_active
-inserted_by
-updated_by
-created_at
-updated_at


Wishlist
-id
-user_id
-product_id
-is_active
-inserted_by
-updated_by
-created_at
-updated_at
