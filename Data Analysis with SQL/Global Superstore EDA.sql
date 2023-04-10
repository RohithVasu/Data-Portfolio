-- Global SuperStore - EDA

-- Checking the data count
 select COUNT(*)
 from SuperStore..Orders;

-- Order the data by Row ID
 select *
 from SuperStore..Orders
 order by 1;

 -- Checking if Order ID is primary key
 select [Order ID], COUNT(*)
 from SuperStore..Orders
 group by [Order ID]
 having COUNT(*) > 1
   
 -- Checking the Order ID
 select *
 from SuperStore..Orders
 where [Order ID] = 'AE-2011-9160'

 -- Checking both Row ID and Order ID
 select [Order ID], [Row ID], COUNT(*)
 from SuperStore..Orders
 group by [Order ID], [Row ID]
 having COUNT(*) > 1

 -- Checking shipping data and order date
 select *
 from SuperStore..Orders
 where [Ship Date] < [Order Date]

 -- Distinct ship modes
 select distinct [Ship Mode]
 from SuperStore..Orders

 -- Minimum and maximum number of days taken for delivery in first class shipping
 select MIN(a.NumOfDays), MAX(a.NumOfDays)
 from(
 select DATEDIFF(DAY, [Order Date], [Ship Date]) as NumOfDays, *
 from SuperStore..Orders
 where [Ship Mode] = 'First Class')a

  -- Minimum and maximum number of days taken for delivery in standard class shipping
 select MIN(a.NumOfDays), MAX(a.NumOfDays)
 from(
 select DATEDIFF(DAY, [Order Date], [Ship Date]) as NumOfDays, *
 from SuperStore..Orders
 where [Ship Mode] = 'Standard Class')a

 -- Number of customers in each region
 select Region, COUNT(*)
 from SuperStore..Orders
 group by Region