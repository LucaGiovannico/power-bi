---
slug: 5-formule-dax-da-conoscere
lang: en
title: 5 DAX formulas worth knowing in Power BI
card_title: 5 DAX formulas worth knowing
description: Five essential DAX formulas for working more effectively in Power BI, with practical examples using CALCULATE, FILTER, SUMX, DIVIDE and SELECTEDVALUE.
card_description: Five DAX formulas and patterns that frequently appear in Power BI models, explained with practical examples.
category: DAX
date: 2026-10-24
reading_time: 7
image: ../assets/images/blog/5-formule-dax-da-conoscere.png
image_alt: Editorial DAX visual featuring five essential formulas for Power BI
image_fit: contain
featured: false
published: true
---

Learning DAX does not mean memorizing dozens of functions.

In most Power BI models, some formulas and patterns appear far more often than others. Understanding them properly makes it easier to build readable measures, manage filter context correctly, and solve calculations that go beyond a simple sum.

In this article, we look at five particularly useful DAX functions: CALCULATE, FILTER, SUMX, DIVIDE and SELECTEDVALUE.

They are not the only functions worth knowing, but they provide a strong foundation for understanding how DAX works.

## 1. CALCULATE: change the context of a calculation

CALCULATE is probably one of the most important functions in DAX.

Its role is to evaluate an expression while modifying the filter context in which that expression is calculated.

Suppose we already have this measure:

```DAX
Total Sales =
SUM(
    Sales[Sales Amount]
)
```

and we want to calculate sales for the Italian market only:

```DAX
Sales Italy =
CALCULATE(
    [Total Sales],
    Customer[Country] = "Italy"
)
```

The original measure does not change. CALCULATE changes the context in which it is evaluated by applying a filter to the country.

This principle is behind a large number of DAX calculations: period comparisons, percentages of totals, filtered KPIs, segment analysis, and measures that need to ignore or replace specific filters.

The key point is therefore not to think of CALCULATE simply as a function that adds a condition.

CALCULATE gives you control over the context in which a measure is evaluated.

## 2. FILTER: build more complex conditions

FILTER returns a table containing only the rows that meet a specified condition.

It is useful when the required filter cannot be expressed clearly enough with a simple condition, or when a condition needs to be evaluated row by row.

For example, we can calculate sales generated only by transactions above 1,000:

```DAX
High Value Sales =
CALCULATE(
    [Total Sales],
    FILTER(
        Sales,
        Sales[Sales Amount] > 1000
    )
)
```

FILTER iterates through the specified table, evaluates the condition for each row, and returns only the rows that satisfy it.

It is a powerful function, but that does not mean it should automatically be used every time a filter is required.

When CALCULATE can use a simple Boolean expression directly, that solution is often clearer.

FILTER becomes especially useful when the logic is more complex, when working with a derived table, or when the condition requires row-by-row evaluation.

This distinction matters because effective DAX is not only about producing the correct result, but also about building measures that remain understandable and maintainable.

## 3. SUMX: evaluate an expression row by row

SUM and SUMX may look similar, but they solve different problems.

SUM directly adds the values stored in a column.

SUMX, on the other hand, is an iterator: it evaluates an expression for every row of a table and then adds the resulting values.

Imagine we have quantity, unit price and unit cost, and we want to calculate total gross margin:

```DAX
Gross Margin =
SUMX(
    Sales,
    Sales[Quantity]
        * (
            Sales[Unit Price]
            - Sales[Unit Cost]
        )
)
```

For each row in the Sales table, the margin for that individual transaction is calculated. Only after that are all the results added together.

This makes SUMX particularly useful when the value we need does not already exist as a column ready to be summed.

The same principle can be applied to calculated revenue, costs, margins, weighted values, and many other indicators.

Understanding iterator functions is an important step in learning DAX because it introduces the concept of row context clearly.

## 4. DIVIDE: handle ratios more reliably

Dashboards and reports constantly use ratios between measures: margin percentage, conversion rate, share of total, growth, rates, and other KPIs.

A division can be written simply with the `/` operator.

In many cases, however, DIVIDE makes the calculation more robust because it directly handles situations where the denominator is zero or blank.

For example:

```DAX
Conversion Rate =
DIVIDE(
    [Orders],
    [Leads]
)
```

If `[Leads]` is zero or BLANK, DIVIDE returns BLANK by default instead of requiring a manual check on the denominator.

An alternative result can also be specified:

```DAX
Conversion Rate =
DIVIDE(
    [Orders],
    [Leads],
    0
)
```

In this case, when the division cannot be performed, the measure returns zero.

Choosing between BLANK and zero is not only a technical decision.

In a report, it can change how the result is interpreted: zero means the KPI actually has a value of zero, while BLANK may indicate that the conditions required to calculate it do not exist.

Even a seemingly simple function such as DIVIDE can therefore help make measures more reliable and semantically accurate.

## 5. SELECTEDVALUE: use the user's selections

SELECTEDVALUE is particularly useful in interactive reports.

It returns the value of a column when the current context contains exactly one distinct value. If there is no single value, it can return an alternative result.

For example:

```DAX
Selected Region =
SELECTEDVALUE(
    Geography[Region],
    "Multiple regions"
)
```

If the user selects one region, the measure returns the name of that region.

If several regions are selected, or the context does not identify one single value, the text `Multiple regions` is returned.

This pattern is very useful for creating dynamic titles, contextual messages, and indicators that react to slicer selections.

For example, a card can display the geographic area currently being analyzed, or a title can automatically change according to the selected segment.

SELECTEDVALUE therefore helps connect DAX logic with the way users interact with a report.

## What actually changes in everyday work

These five functions solve different problems, but together they cover a significant part of the calculations that appear in typical Power BI projects.

CALCULATE provides control over filter context.

FILTER allows you to build subsets of data when conditions become more complex.

SUMX evaluates expressions row by row.

DIVIDE makes ratios and percentages more robust.

SELECTEDVALUE allows measures to react more intelligently to user selections.

The real step forward comes when functions stop being treated as isolated tools and start being combined.

A real-world measure may use CALCULATE together with FILTER, depend on a result produced with SUMX, or change its behavior according to a selection retrieved through SELECTEDVALUE.

These combinations are where DAX becomes an analytical modeling tool rather than simply a language for writing formulas.

## In summary

Working effectively with DAX does not require knowing every available function immediately.

It is much more useful to understand a small number of fundamental concepts deeply and learn when to use them.

CALCULATE is essential for understanding filter context. FILTER allows you to build more complex conditions. SUMX introduces row-by-row evaluation. DIVIDE makes ratios and percentages more reliable. SELECTEDVALUE connects calculations to the context selected by the user.

Mastering these five tools does not mean mastering all of DAX, but it provides a practical foundation for reading, writing, and reasoning about more structured Power BI measures.