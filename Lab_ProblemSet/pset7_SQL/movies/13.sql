--8行目コメントのすべてのmovie.idを手がかりにpeople.nameを探す
SELECT DISTINCT people.name FROM people
JOIN stars
ON stars.person_id = people.id
JOIN movies
ON movies.id = stars.movie_id
WHERE people.name != 'Kevin Bacon' AND movies.id IN
( -- まずKevin Baconが出演したすべてのmovie.idを取得
SELECT movies.id FROM movies
JOIN stars
ON stars.movie_id = movies.id
JOIN people
ON people.id = stars.person_id
WHERE people.name = 'Kevin Bacon' AND people.birth = 1958
);
