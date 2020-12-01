.print Question 1 - sumitro

select distinct uid
from ubadges inner join badges using (bname)
where type = 'gold'

intersect

select q.poster
from (questions inner join posts using (pid)) q

