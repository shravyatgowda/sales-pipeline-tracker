-- How long do deals take to close, and does discounting speed them up?
SELECT
    d.stage,
    d.discount_pct,
    COUNT(*)                                                         AS deals,
    ROUND(AVG(julianday(d.closed_date) - julianday(d.created_date)), 1) AS avg_days_to_close
FROM deals d
WHERE d.closed_date IS NOT NULL
GROUP BY d.stage, d.discount_pct
ORDER BY d.stage, d.discount_pct;
