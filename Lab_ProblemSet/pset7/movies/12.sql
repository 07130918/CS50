SELECT movies.title FROM movies
JOIN stars
ON stars.movie_id = movies.id
JOIN people
ON people.id = stars.person_id
WHERE people.name IN ('Johnny Depp', 'Helena Bonham Carter')
GROUP BY movies.title
HAVING COUNT(movies.title) > 1;
