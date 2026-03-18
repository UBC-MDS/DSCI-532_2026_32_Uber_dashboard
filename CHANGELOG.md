# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-03-17

### Added   

### Changed

### Fixed

### Known Issues

- <!-- Anything incomplete or broken TAs should be aware of (so it isn't mistaken for unfinished work). -->

### Release Highlight: Chart-Based Vehicle Selection

### Collaboration

<!-- Summary of workflow or collaboration improvements made since M3. -->

- **CONTRIBUTING.md:** <!-- Link to the PR that updated it with your M3 retrospective and M4 norms. -->
- **M3 retrospective:** <!-- What changed in your workflow after M3 collaboration feedback. -->
- **M4:** <!-- What you tried or improved this milestone. -->

### Reflection

**Tests:**
- `test_data_wrangling` verifies that the data wrangling prepares the data as expected for the sunburst chart. May fail if the data wrangling process changes.
- `test_vehicle_select` verifies that the vehicle selection results in the correct number for the 'Total Bookings' KPI. May fail if the vehicle selection logic changes.
- `test_date_slider` verifies that the date range slider works with the vehicle selection to filter the dashboard view. May fail if the date range filter logic changes.
- `test_reset_button` verifies that the reset button makes sure the dashboard renders based on the default state of the data after the date range slider and vehicle selection were set. May fail if the reset button logic changes.
<!-- Standard (see General Guidelines): what the dashboard does well, current limitations,
     any intentional deviations from DSCI 531 visualization best practices. -->

<!-- Trade-offs: one sentence on feedback prioritization - full rationale is in #<issue> and ### Changed above. -->

<!-- Most useful: which lecture, material, or feedback shaped your work most this milestone,
     and anything you wish had been covered. -->

---

## [0.4.0] - 2026-03-17
This release introduces a database‑backed data pipeline with Parquet caching, 
a dedicated data wrangling module, and a suite of automated tests, 
while also refining UI interactions, filters, and chart readability across the dashboard.

### Added
- Implemented an automated CSV‑to‑Parquet conversion pipeline: on first run, the raw `ncr_ride_bookings.csv` file is 
  converted to `data/processed/ncr_ride_bookings.parquet` using PyArrow for faster subsequent loads. 
- Created a cleaned Parquet dataset `(ncr_ride_bookings_clean.parquet)` that applies standardized column names, date parsing, and dtype cleaning, and serves as the source for the Ibis/DuckDB table
- Ensured the `data/processed/` subdirectory is created automatically if it does not already exist, simplifying first‑time setup
- Migrated data access from direct CSV loading to a DuckDB + Ibis workflow, enabling database‑backed analytics and caching of processed data for improved performance and scalability
- Added ibis-framework and duckdb to the environment configuration and Python requirements to support the new data processing pipeline.
- Introduced a dedicated data_wrangling function in `src/data_wrangling.py` to centralize data cleaning (column standardization, date conversions, unified Issue_Reason column, dtype enforcement).
- Added `tests/test_data_wrangling.py` to validate that Issue_Reason is correctly generated and mapped to source columns for each booking status, ensuring data integrity for visualizations.
- Added Playwright‑based UI tests for key interactions:
  - Vehicle selection updates the “Total Bookings” KPI `(tests/test_vehicle_select.py)`.
  - Date range slider filters data and updates “Total Revenue” `(tests/test_date_slider.py)`.
  - Reset button restores default state and KPI values `(tests/test_reset_button.py)`.
- Added click interaction on the vehicle pie chart and bar chart so that clicking a category filters the underlying reactive data and updates the line chart, booking status breakdown, and KPIs accordingly.
- Added instructions in `README.md` for installing `pytest-playwright` and running Playwright tests (including headed mode and demo access instructions).
- Added a dark mode


### Changed
- For smaller slices in the pie chart, labels are positioned outside the chart with arrows pointing to the corresponding slice. This improves readability and ensures that the text remains legible even for small proportions.
- In the Booking Status Breakdown visualization, abbreviated labels are used to reduce visual clutter. A codebook (legend) is provided below the figure to clearly define each abbreviation.
- The explicit “All” option in the vehicle type filter was removed and replaced with an empty default selection. When no vehicle type is selected, the dashboard automatically displays data for all vehicle types.
- Updated plot titles and axis labels (e.g., bar chart and “Total Booking Value Over Time” line chart) to be more descriptive and context‑aware
- Updated the main navigation labels, renaming the opening tab from “Original Dashboard” to “Home” and the AI tab from “AI‑powered dashboard” to “AI‑powered” for concision
- Updated the specification document (stories, reactivity diagram, etc.) to reflect new interactive elements such as the clickable pie chart and bar chart.
- Updated the date range slider to include time_format = "%Y-%m-%d" and timezone = "UTC" so that timestamps are hidden from labels and dates are displayed clearly.
- Made chart titles and subtitles reactive to user selections (e.g., clicked vehicle type), so that users can more easily understand which subset of data is being displayed.

### Fixed
- Increased font size in Revenue Distribution by Vehicle Type.
- Increased font size in Booking Status Breakdown sunburst chart. 
- Resolve the issue of cut off in In Uber XL rateing  in bar chart "Avg Driver Rating by Vehicle Type".
- Moving Average appled to smooth the line plot "Total Booking Value Over Time".
- Repositioned the Sunburst plot and increased font sizes for better readability.
- Adjusted spacing, margins, and gaps for a cleaner layout.
- Resolved the issue of booking value y-axis not showing in full.

### Known Issues
- Layout sizing is not fully responsive; components may appear larger or smaller depending on the device screen size.
- The LLM feature occasionally crashes or fails to load; a page refresh resolves this
---

### Release Highlight: [Click-to-Filter Vehicle Interaction]

The advanced feature for this milestone is click-based vehicle type filtering, 
which lets users filter the entire dashboard by clicking on a vehicle segment in the
pie chart or a bar in the vehicle bar chart, rather than relying solely on dropdown controls. 
When a user clicks a slice or bar, the underlying reactive data is filtered to that vehicle type, 
and the line chart, booking status breakdown, KPIs, and titles update to reflect the selected subset, 
making exploration feel more direct and intuitive.

Option chosen: D (Component click event interaction)

PR: #96

Why this option over the others: We prioritized Option D because it delivers the most immediately visible gain in exploratory power for non-technical users: 
a single click on a chart now behaves like a filter control, reducing friction compared to form-based inputs and making it easier to 
“follow your curiosity” through the data. Options A–C are valuable, but they primarily deepen the AI/QueryChat experience, 
whereas our user feedback and prioritization issue (#79) emphasized improving core visual interactivity and clarity in the main dashboard first.

- **Feature prioritization issue link:** [#79](https://github.com/UBC-MDS/DSCI-532_2026_32_Uber_dashboard/issues/79)


### Collaboration

CONTRIBUTING.md: Updated in PR #102 with our M3 retrospective, new M4 collaboration norms, including review requirements and spec‑first changes.

M3 retrospective: After M3, we recognized that some PRs were merged without review, occasionally bundled unrelated changes, 
and did not always sync with the spec documents, which hurt traceability and team awareness. 
We documented these issues explicitly in the retrospective and used them to define concrete M4 norms 
(mandatory reviewer, commit relevance checks, spec updates before code).

M4: In M4 we enforced that every PR is reviewed by a teammate who did not open it, 
checked that commits are scoped to the issue at hand, and required spec updates ahead of implementation, 
which led to cleaner diffs, fewer surprises in review, and better alignment between the app, tests, and documentation. 

### Reflection

The dashboard presents booking and revenue insights through clear visualizations and an organized layout, enabling users to quickly identify 
trends such as revenue distribution by vehicle type and booking status. Interactive charts and consistent styling improve readability and usability. 
However, some limitations remain, including limited filtering options and relatively simple interaction patterns, 
which may restrict deeper exploration of the data. Minor deviations from DSCI 531 visualization best practices were made to maintain 
layout clarity and prioritize readability within the available dashboard space.

- Users can modify the date range to view filtered results for total bookings, total revenue, and canceled bookings within the selected period. The pie chart also displays the percentage distribution of bookings by vehicle type based on the selected filters.
- The dashboard presents the average driver rating by vehicle type as a bar chart, with the ability to filter for one or multiple vehicle categories while maintaining a consistent color scheme across the dashboard.
- The sunburst chart allows users to explore the proportional breakdown of completed versus canceled bookings, including cancellation sources and reasons.
- Users can query the dataset using natural language through an integrated LLM chat feature, with two reactive dashboard elements updating dynamically based on the generated responses.
- The currently filtered dataset can be downloaded directly from the dashboard using a download button.

Compared to M3:

- Data handling was improved by converting the dataset to Parquet format and querying it using DuckDB, which significantly enhances data loading and filtering performance.
- Automated test cases were introduced to validate core filtering logic and key dashboard behaviors, helping ensure stability as the project evolves.
- A component click-event interaction feature was implemented, allowing the dashboard to respond to user interactions with visual components and enabling more dynamic exploratory analysis.
- The internal application structure was refined to support performance improvements, testing, and interactive features, resulting in a more maintainable and robust architecture.
- Several UI refinements were introduced to improve readability and reduce visual clutter, including layout adjustments, clearer labeling, and improved chart presentation.

Overall, version 0.4.0 represents a significant improvement in the dashboard’s performance, interactivity, and maintainability, strengthening its technical foundation for future development.

**Trade-offs:** We prioritized improvements that enhanced readability and visual clarity (such as font sizing and chart labeling) over implementing additional advanced features due to time and milestone constraints.

**Most useful:** Lecture materials on effective dashboard design and visualization best practices were particularly helpful in guiding layout decisions and improving chart readability. Feedback from earlier milestones also helped identify areas where visual clarity and labeling could be improved.

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
