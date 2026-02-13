## Section 1: Motivation and Purpose

> **Our role:** Data scientist consultancy firm
> **Target audience:** UBER/Ride Share Platforms 


> Ride-sharing operates on thin margins, so inefficiencies quickly reduce profitability and trust. In 2024, only 65.96% of bookings in the dataset provided to us by UBER were completed, while roughly 25% were cancelled. Each cancellation represents lost revenue, lower driver utilization, and potential dissatisfaction. Performance likely varies by vehicle type, payment method, time period, and service conditions, making it difficult to pinpoint root causes.
To address this, our team proposes an interactive dashboard that will analyze 2024 performance. It will track key metrics such as total bookings, revenue, completion and cancellation rates, ratings, and ride volume over time, and will allow end users (UBER) to filter by date and vehicle type to compare categories and identify trends. This tool will help managers detect inefficiencies, reduce cancellations, and optimize fleet allocation and pricing strategies.
> As a consultancy our goal is to suppor UBER’s regional operations and performance teams. We believe our dashboard will help UBER improve ride efficiency, reduce cancellations, and maximize revenue while maintaining high customer satisfaction across vehicle categories.

## Section 2: Description of the Data

> Our data originates from an Uber Ride Analytics Dataset from 2024 that was found on Kaggle, the dataset contains 148,770 ride bookings across the full year and 21 operational variables. Each row represents a single booking, covering ride characteristics, financial outcomes, cancellations, and customer satisfaction via ratings.
> Moreover, the dataset includes date, time, booking status, and vehicle type, enabling analysis of ride volume trends and category performance. Financial fields such as booking value and payment method allow revenue calculation and channel comparisons. Operational metrics like average driver arrival time (VTAT) and trip duration (CTAT) measure service efficiency.
> Crucially, the data distinguishes between customer- and driver-initiated cancellations with specific reasons, helping explain incomplete rides and driver and customer ratings provide insight into service quality and popularity by vehicle type.
> Using these variables, we will compute key metrics such as total bookings, completion and cancellation rates, revenue, and average ratings, while analyzing trends over time and across vehicle types to support data-driven operational decisions.
