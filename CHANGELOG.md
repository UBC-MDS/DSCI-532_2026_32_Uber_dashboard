# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.3.0] - 2026-02-28
This release expands more advanced layout edited and some issues fixed and QueryChat Feature added.

### Added
- QueryChat Feature 
- Ability to filter data using querychat (LLM)
- A download csv feature and button for filtered data
- Two reactive elements based on filtered data from LLM
- 

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

---

## Reflection

### Job Stories Status

**Fully Implemented**

- ...#todo


**Partially Implemented**
- 

**Pending for M4**
- Performance optimization.


---

### Layout Comparison: 

Compared to the original M2 sketch:
- ...
- The overall page structure is now more consistent.
- The layout has a better design with larger fonts that makes it more readable for user.
- Styling and spacing were adjusted.
- Colors are now adjusted to convey the information better. 


### Changed
- change the order of components to have fonts larger
- 
---

### Overall Reflection
Version 0.3.0 in Milestone 3 is equipped with Chatbot feature.
...#todo


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