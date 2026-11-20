DELETE FROM daily_summary WHERE order_date = '{{ ds }}';
INSERT INTO daily_summary (order_date, total_orders, total_revenue)
SELECT order_date, COUNT(*), SUM(revenue)
FROM raw_orders
WHERE order_date = '{{ ds }}'
GROUP BY order_date;
