-- Weekly won revenue per region (the "weekly status report" table)
SELECT
    strftime('%Y-W%W', d.closed_date) AS week,
    r.region_name,
    COUNT(*)                          AS deals_won,
    ROUND(SUM(d.deal_value), 0)       AS won_revenue
FROM deals d
JOIN regions r ON r.region_id = d.region_id
WHERE d.stage = 'Won'
GROUP BY week, r.region_name
ORDER BY week, r.region_name;
