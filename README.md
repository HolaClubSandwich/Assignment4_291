SELECT p.Neighbourhood_Name, SUM(c.Incidents_Count), (SUM(c.Incidents_Count) / (p.CANADIAN_CITIZEN + p.NON_CANADIAN_CITIZEN + p.NO_RESPONSE)) as 'Ratio'
FROM crime_incidents c, population p
WHERE c.Year >= 2014 AND c.Year <= 2015 AND p.Neighbourhood_Name = c.Neighbourhood_Name
GROUP BY p.Neighbourhood_Name
