SELECT p.Neighbourhood_Name, SUM(c.Incidents_Count), cast(SUM(c.Incidents_Count) as float) / cast((p.CANADIAN_CITIZEN + p.NON_CANADIAN_CITIZEN + p.NO_RESPONSE) as float) as 'Ratio', (p.CANADIAN_CITIZEN + p.NON_CANADIAN_CITIZEN + p.NO_RESPONSE) as "Pop"
FROM crime_incidents c, population p
WHERE Pop != 0 AND c.Year >= 2014 AND c.Year <= 2015 AND p.Neighbourhood_Name = c.Neighbourhood_Name 
GROUP BY p.Neighbourhood_Name
ORDER BY ratio
