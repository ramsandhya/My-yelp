## Optimize Lookup Time

1. Write a query to find a restaurant by name, note the query run time.

select
	*
from
	restaurant
where name = 'Schaefer Group';

Note the query run time. It takes more than 236 ms to run.

2. Re-run query with explain, and save the explain plan.

Seq Scan on restaurant  (cost=0.00..19218.00 rows=16 width=23)
  Filter: ((name)::text = 'Schaefer Group'::text)

3. Create an index the restaurants name column. This may take a few minutes to run.

4. Reran the command 1

It took 4 ms to run.

5. Reran the query with explain:

explain
select
	*
from
	restaurant
where name = 'Schaefer Group';

Bitmap Heap Scan on restaurant  (cost=4.55..66.41 rows=16 width=23)
  Recheck Cond: ((name)::text = 'Schaefer Group'::text)
  ->  Bitmap Index Scan on restaurant_name_idx  (cost=0.00..4.54 rows=16 width=0)
        Index Cond: ((name)::text = 'Schaefer Group'::text)


## Optimize Sort Time

1. Write a query to find the top 10 reviewers based on karma. Note the query run time.

select
	*
from
	reviewer
order by karma desc
limit 5;

Took 274 ms to run

2. Re-run query with explain, and save the explain plan.

Limit  (cost=33313.64..33313.65 rows=5 width=23)
  ->  Sort  (cost=33313.64..35813.64 rows=1000000 width=23)
        Sort Key: karma DESC
        ->  Seq Scan on reviewer  (cost=0.00..16704.00 rows=1000000 width=23)


3. Create an index to make the above query faster.

CREATE INDEX on reviewer (karma);

4. Re-run the query in step 1. Is performance improved?

select
	*
from
	reviewer
order by karma desc
limit 5;

Took 1 ms

5. Re-run query with explain. Compare the query plan before vs after the index.

Limit  (cost=0.42..0.69 rows=5 width=23)
  ->  Index Scan Backward using reviewer_karma_idx on reviewer  (cost=0.42..52405.74 rows=1000000 width=23)

## Optimize Join Time

1. Write a query to list the restaurant reviews for a particular restaurant. Note the query run time.

select
    restaurant.id, review.content
from
  restaurant
left outer join
  review on restaurant.id = review.restaurant_id
 where
 	restaurant.name = 'Abbott - Cruickshank';

Took 6.1 seconds

2. Re-run query with explain, and save the explain plan.

Hash Right Join  (cost=33125.00..147594.24 rows=1000010 width=186)
  Hash Cond: (review.restaurant_id = restaurant.id)
  ->  Seq Scan on review  (cost=0.00..44076.10 rows=1000010 width=186)
  ->  Hash  (cost=16718.00..16718.00 rows=1000000 width=4)
        ->  Seq Scan on restaurant  (cost=0.00..16718.00 rows=1000000 width=4)

The query shows the system is doing a sequential scan ie a loop which takes longer time to give result.

3. Write a query to find the average star rating for a particular restaurant. Note the query run time.

select
    restaurant.name,
    sum(case when reviewer.karma is NULL then 0 else reviewer.karma end) as total_karma,
# --  count(reviewer.karma) as karma_count, -> if karma value is NULL it doesn't count.
# --	count(*) as karma_count, -> even if karma value is NULL it counts, it should because the review is not NULL.
	count(*) as karma_count,
    avg(reviewer.karma) as average_karma
from
    restaurant
left outer join
	review on restaurant.id = review.restaurant_id
left outer join
	reviewer on reviewer.id = review.reviewer_id
where
	restaurant.name = 'Abbott - Cruickshank'
group by
    restaurant.name;

Gives different values everytime but I am registering 678 msself.

4. Re-run query with explain, and save the explain plan.

GroupAggregate  (cost=19218.63..67053.16 rows=1 width=23)
  Group Key: restaurant.name
  ->  Nested Loop Left Join  (cost=19218.63..67052.99 rows=16 width=23)
        ->  Hash Right Join  (cost=19218.20..67044.50 rows=16 width=23)
              Hash Cond: (review.restaurant_id = restaurant.id)
              ->  Seq Scan on review  (cost=0.00..44076.10 rows=1000010 width=8)
              ->  Hash  (cost=19218.00..19218.00 rows=16 width=23)
                    ->  Seq Scan on restaurant  (cost=0.00..19218.00 rows=16 width=23)
                          Filter: ((name)::text = 'Abbott - Cruickshank'::text)
        ->  Index Scan using reviewer_pkey on reviewer  (cost=0.43..0.52 rows=1 width=8)
              Index Cond: (id = review.reviewer_id)

5. Create an index - which column should you index? - to make the above queries faster.

CREATE INDEX on review(restaurant_id);

Created index on review table -> restaurant_id column

6. Re-run the query you ran in step 1. Is performance improved?

Took 262 ms

7. Re-run the query you ran in step 3. Is performance improved?

Took 238 ms

8. With explain, compare the before and after query plan of both queries.

GroupAggregate  (cost=0.85..19426.34 rows=1 width=23)
  Group Key: restaurant.name
  ->  Nested Loop Left Join  (cost=0.85..19426.17 rows=16 width=23)
        ->  Nested Loop Left Join  (cost=0.42..19417.68 rows=16 width=23)
              ->  Seq Scan on restaurant  (cost=0.00..19218.00 rows=16 width=23)
                    Filter: ((name)::text = 'Abbott - Cruickshank'::text)
              ->  Index Scan using review_restaurant_id_idx on review  (cost=0.42..12.46 rows=2 width=8)
                    Index Cond: (restaurant.id = restaurant_id)
        ->  Index Scan using reviewer_pkey on reviewer  (cost=0.43..0.52 rows=1 width=8)
              Index Cond: (id = review.reviewer_id)

We can notice there is sequential scan on line 161. So this method will take longer timeself.

So, we create index on
CREATE INDEX on restaurant(name);

Created index in 39.5 seconds

Rerun both the top quries again

Step 1 query took 4 ms
Step 3 query took 3 ms

Reason:



EXTRA
--------


Query to look for reviews for a restaurant based on the restaurant id :

select
    restaurant.id, review.content
from
  restaurant
left outer join
	review on restaurant.id = review.restaurant_id
where
	restaurant.id = 51775;
