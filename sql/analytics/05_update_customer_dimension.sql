UPDATE dim_customer dc
SET customer_segment = r.customer_segment
FROM customer_rfm_segmentation r
WHERE dc.customer_key = r.customer_key;