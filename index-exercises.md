# Database Index Exercises

You will use the schema in my-yelp.sql to create a new database.
Then you will use the datagen.js script to generate lots and lots of data to your database. You will want a couple of millions of rows for each of the 3 tables.

## Optimize Lookup Time

1. Write a query to find a restaurant by name, note the query run time.
2. Re-run query with explain, and save the explain plan.
3. Create an index the restaurant's name column. This may take a few minutes to run.
4. Run the query you ran in step 1. Is performance improved?
5. Re-run query with explain. Compare the query plan before vs after the index. If you still see "Seq Scan" in the query plan, you might still have some work to do.

## Optimize Sort Time

1. Write a query to find the top 10 reviewers based on karma. Note the query run time.
2. Re-run query with explain, and save the explain plan.
3. Create an index to make the above query faster.
4. Re-run the query in step 1. Is performance improved?
5. Re-run query with explain. Compare the query plan before vs after the index.

## Optimize Join Time

1. Write a query to list the restaurant reviews for a particular restaurant. Note the query run time.
2. Re-run query with explain, and save the explain plan.
3. Write a query to find the average star rating for a particular restaurant. Note the query run time.
4. Re-run query with explain, and save the explain plan.
5. Create an index - which column should you index? - to make the above queries faster.
6. Re-run the query you ran in step 1. Is performance improved?
7. Re-run the query you ran in step 3. Is performance improved?
8. With explain, compare the before and after query plan of both queries.

## Bonus: Optimize Join Time 2

1. Write a query to list the names of the reviewers who have reviewed a particular restaurant. Note the query run time and save the query plan.
2. Write a query to find the average karma of the reviewers who have reviewed a particular restaurant. Note the query run time and save the query plan.
3. Is this slow? If it is, create an index to make the above queries faster.
4. Re-run queries. Compare query run times and compare explain's query plans.
