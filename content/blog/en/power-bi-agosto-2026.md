---
slug: power-bi-agosto-2026
lang: en
title: Power BI August 2026: 6 updates you should know
card_title: Power BI August 2026: 6 updates you should know
description: The main Power BI August 2026 updates explained in practical terms, from the new theme experience to semantic model refresh controls.
card_description: The most relevant Power BI updates and how they can affect everyday work.
category: POWER BI
date: 2026-10-21
reading_time: 6
image: ../assets/images/blog/power-bi-agosto-2026.png
image_alt: Editorial visual for Power BI August 2026 featuring six key updates
featured: true
published: true
---

Power BI continues to evolve quickly, but not every new feature has the same impact on everyday work.

The August 2026 update introduces several useful improvements for professionals who build reports, manage semantic models, or work on more structured Power BI projects.

In this article, we look at six updates worth paying attention to and, more importantly, what they can actually change in day-to-day work.

## 1. Modern Visual Defaults and the new Theme pane

One of the most visible changes concerns report styling.

Modern Visual Defaults and the new Theme pane are now generally available. New reports use the Fluent 2 base theme, while the Theme pane provides a centralized way to manage color palettes, typography, visual properties, page settings, and the appearance of the filter pane.

This means fewer repetitive formatting changes and greater visual consistency, especially in business reports with many pages and multiple visualizations.

The benefit is therefore not only aesthetic. A more centralized approach to styling also makes it easier to maintain a consistent visual identity over time.

## 2. Date Picker for slicers

The Date Picker for slicers is now generally available.

It combines relative date selections with a calendar and slider, allowing users to select either date ranges or a single date.

With the Single date option, the slicer can be restricted to one day at a time, while selections can be cleared directly from the header.

It may seem like a simple improvement, but it can be particularly useful in operational dashboards where time filtering is one of the most frequent user interactions.

A clearer date-selection experience means less ambiguity and more intuitive report navigation.

## 3. More control over semantic model refresh

One of the most interesting updates concerns semantic model refresh in the Power BI Service.

Previously, the Refresh command would normally perform both schema synchronization and data refresh. Three separate operations are now available:

- Refresh schema and data
- Sync schema only
- Refresh data only

Refresh can also be performed at individual table level.

This provides much more precise control over complex models. For example, if a source changes its schema but only the data needs to be refreshed, it is no longer necessary to automatically perform both operations.

For professionals managing complex semantic models, being able to refresh only what is actually required can reduce unnecessary operations and make maintenance easier to control.

## 4. OneLake images and files directly in reports

Power BI can now use OneLake file URLs as a source for several report elements.

Images stored in OneLake can be used in image visuals, table and matrix cells, cards, slicers, and custom icons.

Some files used in map visuals can also be linked directly through OneLake.

This is especially useful in Microsoft Fabric environments because it allows assets and files to remain within a more governed infrastructure instead of necessarily relying on external public resources.

For organizations centralizing data and content in OneLake, even this relatively small change contributes to a more integrated ecosystem.

## 5. Copilot can understand visuals hidden by bookmarks

Copilot Summary and Copilot Narrative can now take into account visuals that are initially hidden and later displayed through bookmarks.

This is particularly useful in reports that use bookmarks to create tabs, alternative views, or dynamic interfaces.

Previously, a visual hidden in the initial state might not have been considered in the summary. Copilot can now include it in its analysis without changing the bookmark state currently displayed to the user.

Security rules such as RLS and OLS continue to be respected.

For professionals building more interactive reports, this means Copilot can have a more complete understanding of the content actually available on the page.

## 6. Faster PBIP workflows with Visual Studio Code

Microsoft continues to make Power BI Projects more aligned with standard software development workflows.

With PBIP projects, files can now be edited outside Power BI Desktop and detected changes can be applied quickly without restarting the application.

Power BI Desktop also provides direct access to open the project in Visual Studio Code.

For structured projects, this makes it more natural to work with external editors, version control, and development tools.

This is an important step because it reinforces a clear direction: Power BI is no longer only a tool for building visualizations, but is increasingly suited to collaborative and controlled development processes as well.

## What actually changes in everyday work

Not every feature in a monthly update immediately changes the way people work.

In this case, however, several interesting trends emerge.

On one side, Microsoft is improving the report-building experience with more consistent themes, more capable slicers, and new formatting controls.

On the other, it continues to invest in semantic model management, Fabric integration, and developer-oriented workflows.

For professionals working with Power BI, this means the skills required are increasingly moving beyond simply building charts.

Data modeling, user experience design, governance, project organization, and the ability to manage more structured development workflows are becoming increasingly important.

## In summary

Among the August 2026 updates, some can have an immediate impact: the new Theme pane helps maintain visual consistency, the Date Picker improves interaction with time-based data, and the new refresh controls provide more precise management of semantic models.

OneLake, Copilot, and the evolution of PBIP projects point to a broader trend: Power BI is becoming increasingly integrated with the Microsoft Fabric ecosystem and increasingly suitable for structured, collaborative, and governed projects.

The goal is not to use every new feature as soon as it is released, but to understand which updates can genuinely improve the way a report is designed, maintained, and used.