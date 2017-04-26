-- sql to check tne search main files
USE hbnb_dev_db;

-- main 0
SELECT count(*)
FROM places;

--main 1
SELECT count(*)
FROM places
WHERE places.city_id in (
      SELECT cities.id
      FROM cities
      WHERE cities.name in ("Urbana", "Chicago", "Peoria", "Naperville", "San Francisco", "Fremont", "San Jose", "Sonoma", "New Orleans", "Baton Rouge", "Meridian", "Miami", "Tempe", "Calera", "Akron", "Portland"));

--main 2
