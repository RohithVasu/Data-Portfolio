select *
from orders;

-- Top 10 highest revenue generating product

select top 10 product_id, cast(sum(sale_price) as decimal(10, 2)) as sales
from orders
group by product_id
order by sales desc;


-- Top 5 highest selling products in each region

with region_sales as (
	select region, product_id, cast(sum(sale_price) as decimal(10, 2)) as sales
	from orders
	group by region, product_id
),
sales_rank as (
	select *, row_number() over(partition by region order by sales desc) as rank
	from region_sales
)
select region, product_id, sales
from sales_rank
where rank <= 5;


-- Month over month growth comparison for sales for the year 2022 and 2023

with monthly_sales as (
	select year(order_date) as order_year, month(order_date) as order_month, 
		cast(sum(sale_price) as decimal(10, 2)) as sales
	from orders
	group by year(order_date), month(order_date)
)
select 
	order_month,
	sum(case when order_year = 2022 then sales else 0 end) as sales_2022,
	sum(case when order_year = 2023 then sales else 0 end) as sales_2023
from monthly_sales
group by order_month
order by order_month;


-- For each category which month had the highest sales

with monthly_sales as (
	select category, format(order_date, 'yyyy-MM') as order_year_month, 
		cast(sum(sale_price) as decimal(10, 2)) as sales
	from orders
	group by category, format(order_date, 'yyyy-MM')
)
select category, order_year_month, sales
from (select *, row_number() over(partition by category order by sales desc) as rank
		from monthly_sales) rn
where rank = 1;


--which sub category had highest growth by profit in 2023 compare to 2022

with subcategory_sales as (
	select sub_category, year(order_date) as order_year,
		cast(sum(sale_price) as decimal(10, 2)) as sales
	from orders
	group by sub_category,year(order_date)
),
subcat_yearly_sales as (
	select 
		sub_category,
		sum(case when order_year = 2022 then sales else 0 end) as sales_2022,
		sum(case when order_year = 2023 then sales else 0 end) as sales_2023
	from subcategory_sales
	group by sub_category
)
select top 1 *, ((sales_2023 - sales_2022) / sales_2022) * 100 as growth_pct
from subcat_yearly_sales
order by growth_pct desc;