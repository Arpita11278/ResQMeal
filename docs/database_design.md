# Database Design

## Users Table

- user_id
- name
- email
- password
- role
- phone
- address

## Food Table

- food_id
- restaurant_id
- food_name
- quantity
- food_type
- cooked_at
- expiry_time
- status

## NGO Table
- ngo_id	
- user_id	
- ngo_name	
- capacity	
- location

## Requests Table
- request_id	
- food_id	
- ngo_id	
- status

## Delivery Table
- delivery_id	
- request_id	
- partner_id	
- pickup_time	
- delivery_time	
- status

## History
- history_id
- food_id
- delivery_date