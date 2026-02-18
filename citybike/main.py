"""
CityBike — Bike-Sharing Analytics Platform
===========================================

Entry point that orchestrates the full pipeline:
    1. Load raw data
    2. Inspect & clean data
    3. Run analytics (business questions)
    4. Run numerical computations
    5. Generate visualizations
    6. Export summary report

Usage:
    python main.py
"""

from analyzer import BikeShareSystem
from visualization import plot_trips_per_station, plot_monthly_trend, plot_duration_histogram, plot_duration_by_user_type


def main() -> None:
    """Run the complete CityBike analytics pipeline."""

    system = BikeShareSystem()

    # Step 1 — Load data
    print("\n>>> Loading data …")
    system.load_data()

    # Step 2 — Inspect
    print("\n>>> Inspecting data …")
    system.inspect_data()

    # Step 3 — Clean
    print("\n>>> Cleaning data …")
    system.clean_data()

    # Step 4 — Analytics
    print("\n>>> Running analytics …")
    summary = system.total_trips_summary()
    print(f"  Total trips      : {summary['total_trips']}")
    print(f"  Total distance   : {summary['total_distance_km']} km")
    print(f"  Avg duration     : {summary['avg_duration_min']} min")

    # TODO: call additional analytics methods here
    # e.g. system.top_start_stations(), system.peak_usage_hours(), ...

    # Step 4b — Pricing (Strategy Pattern + NumPy vectorized fares)
    # The pricing strategies define the business rules (per-minute rate, etc.),
    # and calculate_fares applies those rates to all trips at once via NumPy.
    
    # Step 4b — Pricing (Strategy Pattern + NumPy vectorized fares)
    print("\n>>> Computing fares …")
    system.compute_fares()

    top5 = system.top_fares(n=5)
    print("\nTop 5 fares:")
    print(top5.to_string(index=False))

    avg_fares = system.avg_fare_by_user_type()
    print("\nAverage fare per user type:")
    print(avg_fares.to_string(index=False, header=False))


    # Step 5 — Visualizations
    print("\n>>> Generating visualizations …")
    plot_trips_per_station(system.trips, system.stations)

    plot_monthly_trend(system.trips)
    plot_duration_histogram(system.trips)
    plot_duration_by_user_type(system.trips)

    # Step 6 — Report
    system.generate_summary_report()

    print("\n>>> Done! Check output/ for results.")


if __name__ == "__main__":
    main()
