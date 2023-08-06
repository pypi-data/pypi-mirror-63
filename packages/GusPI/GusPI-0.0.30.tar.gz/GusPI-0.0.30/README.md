## GusPI
A package to include statistical supports.

Quick start

```
$ python3 -m pip install -U plotly

$ python3 -m pip install -U scikit-learn

$ python3 -m pip install -U GusPI
```

## Demo notebook

[demo](https://colab.research.google.com/drive/1gVJvFCDwf7DxeKtt_jSd5FuEKZSRkvTb)

## GusPI.scraper

The scrape package provides an easy way to scrape Yelp business info and Yelp reviews for specific business.

```
from GusPI import scraper
```

YelpBizInfo
The function collects business info and save it into a csv file.

```
#Example

#declare a list: https://www.yelp.com/biz/`artisan-ramen-milwaukee`
CUISINES = ['artisan-ramen-milwaukee','red-light-ramen-milwaukee-5']

#scrape the business info
scraper.YelpBizInfo(CUISINES)
```

YelpReview
The function collects reviews for respective business and save them into separate files by business names.
```
#Example

#declare a list: https://www.yelp.com/biz/`artisan-ramen-milwaukee`
CUISINES = ['artisan-ramen-milwaukee','red-light-ramen-milwaukee-5']

#scrape the business info
scraper.YelpReview(CUISINES)
```

## GusPI.suPY

```
from GusPI import suPY
```

### metrics

This package provides several analytical formulas to support supply chain analytics.

Economic order quantity
EOQ(demand, mean, STD, C, Ce, Cs, Ct)

Perfect Order Measurement
POM(TotalOrders, ErrorOrders)

Fill Rate
FR(TotalItems, ShippedItems)

Inventory Days of Supply
IDS(InventoryOnHand,AvgDailyUsage)

Freight cost per unit
FCU(TotalFreightCost,NumberOfItems)

Inventory Turnover
IT(COGS,AvgInventory)

Days of Supply (DOS)
DOS(AvgInventory,MonthlyDemand)

Gross Margin Return on Investment (GMROI)
GMROI(GrossProfit, OpeningStock, ClosingStock)

Inventory Accuracy
IA(ItemCounts, TotalItemCounts)

Storage Utilization Rate
SUR(InventoryCube, TotalWarehouseCube)

Total Order Cycle Time
TOCT(TimeOrderReceivedbyCustomer, TimeOrderPlaced,TotalNumberofOrdersShipped)

Internal Order Cycle Time
IOCT(TimeOrderShipped, TimeOrderReceived, NumberofOrdersShipped)

Read sales data from csv file and calculate basic safty sock and reporder point.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 12LS
#safety days: 5
#leadtime in days: 7

suPy.basicSafetyStock('SalesData.csv','12LS',5,7)
```

Read sales data from csv file and calculate basic safty sock and reporder point for all products.

```
#Example

#sales data from a csv file: salesData.csv
#safety days: 5
#leadtime in days: 7

suPy.basicSafetyStockList('SalesData.csv',5,7)
```

Read sales data from csv file and calculate safty sock and reporder point.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 12LS
#service rate: 0.95
#leadtime in days: 7

suPy.safetyStockwtServiceRate('SalesData.csv','12LS',0.95,7)
```

Read sales data from csv file and calculate basic safty sock and reporder point for all products.

```
#Example

#sales data from a csv file: salesData.csv
#service rate: 0.95
#leadtime in days: 7

suPy.safetyStockwtServiceRateList('SalesData.csv',0.95,7)
```

Read sales data from csv file and calculate coefficient of variation of a product.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 12LS
#CV is non-negative and higher CV indicates higher volatility

suPy.cvPerProduct('SalesData.csv','12LS')
```

Read sales data from csv file and calculate 'Intercept', 'Slope', 'Mean Absolute Error', 'Mean Squared Error', 'Root Mean Squared Error' of a product.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 12LS

suPy.linearRegressionPerProduct('SalesData.csv','12LS')
```

Read sales data from csv file and calculate EOQ of a product.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 12LS
#Setup cost: 2000
#Holding cost: 1000

suPy.eoqPerProduct('SalesData.csv','12LS',2000,1000)
```

Read sales data from csv file and create a list of average quantity sold per year for products.

```
#Example

#sales data from a csv file: salesData.csv

suPy.avgQtySoldList('SalesData.csv')
```

Read sales data from csv file and calculate the seasonality index of a product for a given year.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 12LS
#year: 2018

suPy.seasonalityIndexPerProduct('SalesData.csv','22LS',2018)
```

### graphs

Read sales data from csv file and print out a lineplot of a product quantity sold.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 22LS

#print the lineplot
suPy.lineplotQtyByMonth('salesData.csv','22LS')
```

Read sales data from csv file and print out a lineplot of a product's total cost sold.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 22LS

#print the lineplot
suPy.lineplotTotalCostByMonth('salesData.csv','22LS')
```

Read sales data from csv file and print out a lineplot of a product's total sales.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 22LS

#print the lineplot
suPy.lineplotTotalSalesByMonth('salesData.csv','22LS')
```

Read sales data from csv file and print out a lineplot of a product's average cost.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 22LS

#print the lineplot
suPy.lineplotAverageCostByMonth('salesData.csv','22LS')
```

Read sales data from csv file and print out a lineplot of a product's average sales.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 22LS

#print the lineplot
suPy.lineplotAverageSalesPriceByMonth('salesData.csv','22LS')
```

Read sales data from csv file and print out sales forecast for a product.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 22LS
#length in month for the prediction: 12

#print the metrics and lineplot
suPy.forecastQtyMonthlySales('SalesData.csv','12LS',12)
```

Read sales data from csv file and print out pricing forecast for a product.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 22LS
#length in month for the prediction: 12

#print the metrics and lineplot
suPy.forecastMonthlyPrice('SalesData.csv','12LS',12)
```

Read sales data from csv file and print out cost forecast for a product.

```
#Example

#sales data from a csv file: salesData.csv
#product number to perform analysis on: 22LS
#length in month for the prediction: 12

#print the metrics and lineplot
suPy.forecastMonthlyCost('SalesData.csv','12LS',12)
```

## GusPI.finPy

```
from GusPI import finPy
```

Read financial statements from csv file and print them out as a dataframe.

```
#Example

#balancesheet from a csv file: balance_sheet_yr.csv

#print the statement in a dataframe
finPy.printStatement('balance_sheet_yr.csv')
```

Read financial statements from csv files and provide a single line chart for analysis.

```
#Example

#income statement from a csv file: income_statement_m.csv

#print a single line chart
finPy.lineplot('income_statement_m.csv','total_revenue')
```

Read financial statements from csv files and provide multiple line charts for analysis.

```
#Example

#balancesheet from a csv file: balance_sheet_yr.csv

#print multiple lineplots
finPy.multilineplots('balance_sheet_yr.csv', '3 year BalanceSheet Graph')
```

Read financial statements from csv files and provide a bullet chart for analysis.

```
#Example

#balancesheet from a csv file: balance_sheet_yr.csv

#print financial metrics
finPy.bulletChart('balance_sheet_yr.csv','inventory')
```

Read financial statements from csv files and provide financial metrics for analysis.

```
#Example

#balancesheet from a csv file: balance_sheet_yr.csv
#incomeStatement from a csv file: income_statement_3yr.csv

#print financial metrics
finPy.calculateMetrics('balance_sheet_yr.csv','income_statement_12m.csv')
```
