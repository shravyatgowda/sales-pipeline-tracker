-- Best-selling product inside each category, using RANK() over a partition
WITH product_revenue AS (
    SELECT
        p.category,
        p.product_name,
        ROUND(SUM(d.deal_value), 0) AS won_revenue
    FROM deals d
    JOIN products p ON p.product_id = d.product_id
    WHERE d.stage = 'Won'
    GROUP BY p.category, p.product_name
)
SELECT
    category,
    product_name,
    won_revenue,
    RANK() OVER (PARTITION BY category ORDER BY won_revenue DESC) AS rank_in_category
FROM product_revenue
ORDER BY category, rank_in_category;
