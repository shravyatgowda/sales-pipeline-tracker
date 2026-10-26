-- Value still sitting in the open pipeline, by region and stage
SELECT
    r.region_name,
    d.stage,
    COUNT(*)                    AS open_deals,
    ROUND(SUM(d.deal_value), 0) AS pipeline_value
FROM deals d
JOIN regions r ON r.region_id = d.region_id
WHERE d.stage IN ('Lead', 'Qualified', 'Proposal')
GROUP BY r.region_name, d.stage
ORDER BY r.region_name, pipeline_value DESC;
