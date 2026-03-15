# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.4.0] - 2026-03-16
This release expands more advanced feature, added test cases and parquet and also some UI issues fixed.

### Added
- Test cases #todo (need more explainaton)
- Added code to app.py to convert csv to parquet
- Connected to duckDB
- dapted filtering to duckDB on the dashboard
- #todo (the advanced feature)


### Changed
- For smaller slices in the pie chart, labels are positioned outside the chart with arrows pointing to the corresponding slice. This improves readability and ensures that the text remains legible even for small proportions.
- In the Booking Status Breakdown visualization, abbreviated labels are used to reduce visual clutter. A codebook (legend) is provided below the figure to clearly define each abbreviation.
- The explicit “All” option in the vehicle type filter was removed and replaced with an empty default selection. When no vehicle type is selected, the dashboard automatically displays data for all vehicle types.

### Fixed
- Booking Status Breakdown': font too small.
- Resolve the issue of cut off in In Uber XL rateing  in bar chart "Avg Driver Rating by Vehicle Type".
- Moving Average appled to smooth the line plot "Total Booking Value Over Time".
- Repositioned the Sunburst plot and increased font sizes for better readability.
- Adjusted spacing, margins, and gaps for a cleaner layout.
- Resolved the issue of booking value y-axis not showing in full.

### Known Issues
- Adding dark mode switch 
- Performance optimization for larger datasets is pending.
- Layout sizing is not fully responsive; components may appear larger or smaller depending on the device screen size.
- The LLM feature occasionally crashes or fails to load; a page refresh resolves this
---

## Reflection

### Job Stories Status

**Fully Implemented**

- Users can modify the date range to view filtered results for total bookings, total revenue, and canceled bookings within the selected period. Additionally, users can view the percentage distribution of bookings filtered by vehicle type in the pie chart.
- The dashboard displays the average driver rating grouped by vehicle type as a bar chart, with the option to filter for one or multiple specific vehicle categories, using a color scheme consistent with the rest of the dashboard.
- The sunburst plot enables users to examine the percentage breakdown of completed versus canceled bookings, further distinguishing cancellation source and reasons proportionally.
- Users can now query the dataset in natural language via the LLM chat feature, with two reactive dashboard elements responding dynamically to LLM output.
- Users can download the currently filtered dataset directly from the dashboard via the download button.
- #todo

**Partially Implemented**
- Layout responsiveness across device sizes is incomplete; sizing does not yet adapt dynamically to different screen resolutions.

---

### Layout Comparison
Compared to M3:
- Data storage was optimized by converting the dataset to Parquet format and querying it through DuckDB, significantly improving data loading and filtering performance within the dashboard.
- Automated test cases were added to verify key dashboard behaviors and core filtering logic, helping ensure that future changes do not unintentionally break expected functionality.
- An advanced component click-event interaction feature was implemented, enabling the application to react to user interactions with output components (e.g., charts), thereby improving interactivity and enabling more dynamic exploratory analysis.
- The internal application structure was refined to better support performance improvements, testing, and interactive behaviors, contributing to a more robust and maintainable dashboard architecture.

---

### Overall Reflection
Version 0.4.0 represents a major step forward in both functionality and performance of the dashboard. Data handling was significantly improved by converting the dataset to Parquet format and integrating DuckDB for querying, which accelerates data loading and filtering operations and enhances overall responsiveness.

In addition, automated test cases were introduced to verify the core filtering logic and expected behaviors of the dashboard. These tests help ensure that future modifications do not unintentionally break key functionality and provide a clearer framework for maintaining reliability as the project evolves.

The dashboard also gained an advanced component click-event interaction capability, allowing the application to respond dynamically to user interactions with visual components. This enhances exploratory analysis by enabling more interactive workflows directly through the charts and outputs.

Several UI improvements were implemented to increase readability and usability. Layout adjustments, clearer labeling strategies, and refinements to chart presentation help reduce visual clutter and make the dashboard easier to interpret. Together, these changes create a more polished and user-friendly interface while maintaining consistency across visual components.

Overall, this version strengthens the technical foundation of the application by improving performance, interactivity, and maintainability, positioning the dashboard for continued refinement and more advanced analytical capabilities in future iterations.

---

## [0.3.0] - 2026-03-09
This release expands more advanced layout edited and some issues fixed and QueryChat Feature added.

### Added
- QueryChat Feature 
- Ability to filter data using querychat (LLM)
- A download csv feature and button for filtered data
- Two reactive elements based on filtered data from LLM

### Changed
- Changed the rating plot from a dot plot to a bar chart, with colors aligned to match the pie chart palette.
- Reordered dashboard components to prioritize larger, more readable font sizes.
- Applied a distinct color palette to the bottom pie chart for improved visual differentiation.
- Removed the legend from the revenue-by-vehicle-type pie chart to reduce visual clutter.
- Standardized box layouts for greater visual consistency across the dashboard.

### Fixed
- Updated the color scheme in the bottom pie chart.
- Fixed and refined the legend in the top pie chart.
- Aligned the value box icons for consistency.
- Fixed the sidebar so it is no longer scrollable.
- Standardized box layouts throughout the dashboard.
- Repositioned the Sunburst plot and increased font sizes for better readability.
- Reduced the size of value boxes to provide more space for the Sunburst plot.
- Replaced the dot plot with a bar chart to show Average Driver Rating by vehicle category.
- Matched the color palette of the Revenue Distribution pie chart with the new bar chart, ensuring consistent vehicle colors across both plots.
- Adjusted spacing, margins, and gaps for a cleaner layout.
- Resized the AI dashboard page to optimize the Connect Cloud layout.
- Added deployment links for Connect Cloud.

### Known Issues

- Performance optimization for larger datasets is pending.
- Layout sizing is not fully responsive; components may appear larger or smaller depending on the device screen size.
- The "Premier Sedan" bar chart label is slightly cut off in the Connect Cloud deployed version.
- The LLM feature occasionally crashes or fails to load; a page refresh resolves this
---

## Reflection

### Job Stories Status

**Fully Implemented**

- Users can modify the date range to view filtered results for total bookings, total revenue, and canceled bookings within the selected period. Additionally, users can view the percentage distribution of bookings filtered by vehicle type in the pie chart.
- The dashboard displays the average driver rating grouped by vehicle type as a bar chart, with the option to filter for one or multiple specific vehicle categories, using a color scheme consistent with the rest of the dashboard.
- The sunburst plot enables users to examine the percentage breakdown of completed versus canceled bookings, further distinguishing cancellation source and reasons proportionally.
- Users can now query the dataset in natural language via the LLM chat feature, with two reactive dashboard elements responding dynamically to LLM output.
- Users can download the currently filtered dataset directly from the dashboard via the download button.


**Partially Implemented**
- Layout responsiveness across device sizes is incomplete; sizing does not yet adapt dynamically to different screen resolutions.

**Pending for M4**
- Performance optimization.
- Full responsive layout support across device sizes.
- Fix the "Premier Sedan" label clipping on the Connect Cloud deployment.
- Improve LLM reliability to eliminate the need for manual refreshes.
---

### Layout Comparison
Compared to M2:
- Component order was revised to prioritize readability, with larger fonts now more prominent in the layout.
- The sidebar was stabilized by fixing width overflow, eliminating unwanted horizontal scrolling.
- Box layouts were made more consistent in size and spacing, improving the overall visual rhythm of the dashboard.
- Color schemes were refined across multiple charts to improve differentiation and cohesion.

### Changed
- Updated job stories to reflect M3 implementation progress and scope.
- Updated the README to reflect new features and deployment details.
- Improved visual consistency across chart components through coordinated color palettes.
---

### Overall Reflection
Version 0.3.0 represents a significant step forward in interactivity and polish. The addition of LLM-powered querying allows for a new dimension of data exploration, allowing users to ask questions about the dataset directly within the dashboard. The download functionality and reactive elements further strengthen the user workflow.

Layout and visual improvements include the bar chart conversion, color alignment, and sidebar fix, these address the most pressing usability issues carried over from M2. While responsiveness and LLM stability remain slight concerns, the foundation is now well-positioned for final refinement. The focus going forward will be on addressing these known issues, improving cross-device compatibility, and hardening the LLM integration for production reliability. Testing outputs also needs to be done to ensure consistency.

---

## [0.2.0] - 2026-02-28
This release expands core functionality, refines the layout, and improves overall stability as part of the M2 milestone.

### Added

- Add Booking Status Sunburst Plot (PR #39) to address Issue #27.
- An “All” option to the vehicle type dropdown filter to allow users to view aggregated results across all vehicle categories.
- Project demo video demonstrating core functionality and workflow.
- Mermaid diagram to visually represent system structure and workflow.


### Fixed

- Repositioned the vehicle type dropdown menu to improve layout alignment and usability.
- Converted the vehicle type dropdown into a `selectize` element to enhance user interaction and filtering functionality.
- Fixed the reset button to properly restore filters and visualizations to their default state.
- The value box edited and the icon added. 
- The Reset button functionality.


### Known Issues

- The size of the value box components requires further adjustment for better visual balance.
- Font size within the sunburst plot remains too small for optimal readability.
- Performance optimization for larger datasets is pending.

---

## Reflection

### Job Stories Status

**Fully Implemented**

- Users can modify the date range to view filtered results for total bookings, total revenue, and canceled bookings within the selected period. Additionally, users can view the percentage distribution of bookings filtered by vehicle type in the pie chart.
- The dashboard also displays the average driver rating grouped by vehicle type, with the option to filter for one or multiple specific vehicle categories.
- The sunburst plot enables users to examine the percentage breakdown of completed versus canceled bookings. For canceled bookings, the visualization further distinguishes the source of cancellation and the corresponding reasons, each represented proportionally by percentage.

**Partially Implemented**
- 

**Pending for M3**
- To adjust layout elements to improve font clarity in the sunburst plot.
- Performance optimization.


---

### Layout Comparison: 

Compared to the original M1 sketch:
- The overall page structure remains consistent with the initial concept.
- The layout more accurately reflects responsive requirements.
- Navigation placement was adjusted to improve usability and clarity.
- Styling and spacing were adjusted for consistency across views.


### Changed
- Updated job stories to reflect current implementation progress and scope adjustments.
- Updated the README to improve clarity, structure, and project documentation.
- Updated the default plotting theme to improve visual consistency and readability.
- Improved the “Average Driver Rating by Vehicle Type” visualization for clarity and interpretability.

---

### Overall Reflection
Version 0.2.0 represents a structural and functional milestone. The application now supports the core user workflow with improved reliability and layout clarity. 

While the implementation closely follows the M2 specification, refinements were made to improve usability. These changes strengthen the foundation for M3, where the focus will shift to optimization, accessibility, and feature expansion.
