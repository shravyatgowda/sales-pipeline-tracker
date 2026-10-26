-- Win rate and won revenue per region (closed deals only)
SELECT
    r.region_name,
    COUNT(*)                                                     AS closed_deals,
    SUM(CASE WHEN d.stage = 'Won' THEN 1 ELSE 0 END)             AS won_deals,
    ROUND(100.0 * SUM(CASE WHEN d.stage = 'Won' THEN 1 ELSE 0 END) / COUNT(*), 1) AS win_rate_pct,
    ROUND(SUM(CASE WHEN d.stage = 'Won' THEN d.deal_value ELSE 0 END), 0)         AS won_revenue
FROM deals d
JOIN regions r ON r.region_id = d.region_id
WHERE d.stage IN ('Won', 'Lost')
GROUP BY r.region_name
ORDER BY won_revenue DESC;
