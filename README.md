# DSCI-532_2026_32: Uber Dashboard Project
This project develops an interactive dashboard analyzing Uber’s 2024 ride data to evaluate operational performance, revenue trends, and customer satisfaction. The dashboard provides key business insights through visual analytics, helping stakeholders understand ride volume patterns, vehicle type performance, geographic demand distribution, trip duration trends, and customer ratings.

Using Python, Shiny, and interactive visualizations, the project transforms raw ride-level data into meaningful KPIs and decision-support tools. The dashboard enables users to explore trends over time, compare service categories, and identify areas for operational improvement and revenue optimization.

This project demonstrates the full data workflow: data cleaning, exploratory data analysis (EDA), KPI development, and interactive dashboard deployment. It emphasizes business storytelling, data-driven decision-making, and clear visual communication.

## Installations

1.  Fork the repository: https://github.com/UBC-MDS/DSCI-532_2026_32_Uber_dashboard.git

2.  Clone the fork locally using:

``` bash
git clone git@github.com:UBC-MDS/DSCI-532_2026_32_Uber_dashboard.git
```
Then please cd into the root of the repo by:
```bash
cd DSCI-532_2026_32_Uber_dashboard
```

3.  Create the virtual environment with:

``` bash
conda env create -f environment.yml
```

4.  Once the environment is created, activate it with:

``` bash
conda activate ddsci-532_2026_32_Uber_dashboard
```

5.  Run the app locally with:

``` bash
shiny run src/app.py 
```