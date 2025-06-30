SELECT 
    r.region, 
    r.subregion, 
    r.country, 
    s.age,
    s.population
FROM 
    region r
INNER JOIN 
    `simple` s ON r.region_id = s.region_id
WHERE 
    s.year = '2023';
