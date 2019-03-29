# Assignment4_291
291 assignment
SELECT p.Neighbourhood_Name, (p.CANADIAN_CITIZEN + p.NON_CANADIAN_CITIZEN + p.NO_RESPONSE) AS 'Tot' , c.Latitude, c.Longitude FROM population p, coordinates c WHERE p.Neighbourhood_Name = c.Neighbourhood_Name AND Tot != 0 AND c.Latitude != 0 ORDER BY Tot LIMIT :number;", {"number": number}
