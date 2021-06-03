--1. What are the top ten users (user_id’s) and audiobooks (audiobook_id’s) with
--more audio time listened?

select user_id 
, SUM(seconds)
from audiobook_plays ap
group by 1
order by 2 desc 
limit 10;

--2. Calculate the WAU - weekly unique active users (where an active = a user
--that plays an audiobook) for the dates provided in the data.

select 
DATE_TRUNC('WEEK',created_at)::date as WEEK_DAY
, COUNT(distinct user_id) as WAU
from audiobook_plays ap 
group by 1
order by 1 desc;

--3. Calculate the week over week retention rate of active users for the dates
--provided in the data? (a retained user is one that listened to an audiobook in
--week N-1 and also listened again in week N, where N is the week shown in the
--column)

with user_week as (
	select distinct user_id 
	, DATE_TRUNC('WEEK',created_at)::date as week
	from audiobook_plays ap 
)
--
, user_ret_calc as (
	select user_id 
	, week as week_n
	, lag(week) over(partition by user_id order by week asc) as week_n_1
	, case 
		when week - lag(week) over(partition by user_id order by week asc) > 7 
			or lag(week) over(partition by user_id order by week asc) is null 
		then false 
		else true 
	end as ret_user
	from user_week
)
--
select 
ret_week.week_n
--, act_week_n_1.week_n_1
, act_users_n_1
, ret_users_n
, (ret_users_n::float / act_users_n_1::float)*100 as rate
from(
	select week as week_n_1
	, count(distinct user_id) as act_users_n_1
	from user_week
	group by 1
) as act_week_n_1
left join (
	select week_n
	, week_n_1
	, count(distinct user_id) as ret_users_n
	from user_ret_calc
	where ret_user
	group by 1,2
) as ret_week
on ret_week.week_n_1 = act_week_n_1.week_n_1;

--4. What is the average time listened (in hours) per user for the last 30 days for
--the data provided?

select user_id 
, avg(seconds)
from audiobook_plays ap 
where created_at > (select max(created_at- interval '30 days') from audiobook_plays ap2 )
group by 1;

--5.  What has been the month over month growth % for the number of
--audiobook plays?

beekcreate or replace view test as (
with plays as (
	select date_trunc('month',created_at)::date as month
	, count(id) as Q_plays
	, lag(count(id)) over (order by date_trunc('month',created_at)::date) as Q_plays_n_1
	from audiobook_plays ap 
	group by 1
)
select *
, ((q_plays::float - q_plays_n_1::float)/q_plays_n_1::float)*100 as rate
from plays
);

--6.What is the distribution per month of users subscribed based on their first
--audiobook play? (y- axis: count of subscribed users, x: first month of
--audiobook play)

with first_month as (
	select user_id 
	, min(date_trunc('month',ap.created_at)::date) as first_month
	from audiobook_plays ap 
	inner join users u
	on u.id = ap.user_id and has_been_subscribed
	group by 1
)
select first_month 
, count(*)
from first_month
group by 1;

--7.What is the favorite book category for the subscribed user with the most
--listened time?

with max_user as(
select 
ap.user_id 
, sum(seconds) as listened_time
from audiobook_plays ap 
inner join users u 
on ap.user_id = u.id and has_been_subscribed 
group by 1
order by 2 desc
limit 1
)
--
, audiobook_code as(
	select 
	ap.user_id 
	, ap.audiobook_id 
	, book_category_codes
	, unnest(book_category_codes) book_cat_code
	, count(ap.id) q_plays
	, sum(seconds) time_listened
	from audiobook_plays ap
	left join audiobook a
	on a.id = ap.audiobook_id 
	where user_id = (select user_id from max_user)
	group by 1,2,3
) --select * from audiobook_code ;
select 
user_id
, audiobook_id
, book_category_codes
, book_cat_code
, name
, sum(q_plays) q_plays
, sum(time_listened) time_listened
from audiobook_code ac
left join book_categories bc
on bc.book_cateogory_code = ac.book_cat_code
group by 1,2,3,4,5
order by time_listened desc
;

--8. What is the book category that has been showing more popularity? Why and
--how did you picked it?

with audiobook_code as(
	select 
	book_category_codes
	, unnest(book_category_codes) book_cat_code
	, count(ap.id) q_plays
	, sum(seconds) time_listened
	from audiobook_plays ap
	left join audiobook a
	on a.id = ap.audiobook_id 
	group by 1,2
)
select 
book_category_codes
, book_cat_code
, name
, sum(q_plays) q_plays
, sum(time_listened) time_listened
from audiobook_code ac
left join book_categories bc
on bc.book_cateogory_code = ac.book_cat_code
group by 1,2,3
order by time_listened desc
;

--9. Given the following user_id: 950858 and based on the data what would be
--the next audiobook you would recommend? Explain your reasoning!

with audiobook_code as(
	select 
	ap.user_id 
	, ap.audiobook_id 
	, book_category_codes
	, unnest(book_category_codes) book_cat_code
	, count(ap.id) q_plays
	, sum(seconds) time_listened
	from audiobook_plays ap
	left join audiobook a
	on a.id = ap.audiobook_id 
	where user_id = 950858
	group by 1,2,3
)
select 
user_id
, audiobook_id
, book_category_codes
, book_cat_code
, name
, sum(q_plays) q_plays
, sum(time_listened) time_listened
from audiobook_code ac
left join book_categories bc
on bc.book_cateogory_code = ac.book_cat_code
group by 1,2,3,4,5
order by time_listened desc
; 


-- Dashboard

with plays as (
	select * from audiobook_plays ap
)
--
select * from users;