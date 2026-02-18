"""
Data analysis engine for the CityBike platform.

Contains the BikeShareSystem class that orchestrates:
    - CSV loading and cleaning
    - Answering business questions using Pandas
    - Generating summary reports
"""

import pandas as pd
import numpy as np
from pathlib import Path
from pricing import CasualPricing, MemberPricing, PeakHourPricing
from numerical import calculate_fares  


DATA_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
PEAK_HOURS = [(7, 9), (17, 19)]

class BikeShareSystem:
    """Central analysis class — loads, cleans, and analyzes bike-share data.

    Attributes:
        trips: DataFrame of trip records.
        stations: DataFrame of station metadata.
        maintenance: DataFrame of maintenance records.
    """

    def __init__(self) -> None:
        self.trips: pd.DataFrame | None = None
        self.stations: pd.DataFrame | None = None
        self.maintenance: pd.DataFrame | None = None

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def load_data(self) -> None:
        """Load raw CSV files into DataFrames."""
        self.trips = pd.read_csv(DATA_DIR / "trips.csv")
        self.stations = pd.read_csv(DATA_DIR / "stations.csv")
        self.maintenance = pd.read_csv(DATA_DIR / "maintenance.csv")

        print(f"Loaded trips: {self.trips.shape}")
        print(f"Loaded stations: {self.stations.shape}")
        print(f"Loaded maintenance: {self.maintenance.shape}")

    # ------------------------------------------------------------------
    # Data inspection (provided)
    # ------------------------------------------------------------------

    def inspect_data(self) -> None:
        """Print basic info about each DataFrame."""
        for name, df in [
            ("Trips", self.trips),
            ("Stations", self.stations),
            ("Maintenance", self.maintenance),
        ]:
            print(f"\n{'='*40}")
            print(f"  {name}")
            print(f"{'='*40}")
            print(df.info())
            print(f"\nMissing values:\n{df.isnull().sum()}")
            print(f"\nFirst 3 rows:\n{df.head(3)}")

    # ------------------------------------------------------------------
    # Data cleaning
    # ------------------------------------------------------------------

    def clean_data(self) -> None:
        # --- Step 1: Remove duplicate rows ---
        self.trips = self.trips.drop_duplicates(subset=["trip_id"])
        self.stations = self.stations.drop_duplicates(subset=["station_id"])
        self.maintenance = self.maintenance.drop_duplicates(subset=["record_id"])
        print(f"[Step1] Duplicates removed: Trips={self.trips.shape[0]}, Stations={self.stations.shape[0]}, Maintenance={self.maintenance.shape[0]}")

        # --- Step 2: Parse date/datetime columns ---
        self.trips["start_time"] = pd.to_datetime(self.trips["start_time"], errors="coerce")
        self.trips["end_time"] = pd.to_datetime(self.trips["end_time"], errors="coerce")
        self.maintenance["maintenance_date"] = pd.to_datetime(self.maintenance["date"], errors="coerce")

        # --- Step 3: Convert numeric columns stored as strings ---
        self.trips["duration_minutes"] = pd.to_numeric(self.trips["duration_minutes"], errors="coerce")
        self.trips["distance_km"] = pd.to_numeric(self.trips["distance_km"], errors="coerce")
        self.stations["capacity"] = pd.to_numeric(self.stations["capacity"], errors="coerce")
        self.maintenance["cost"] = pd.to_numeric(self.maintenance["cost"], errors="coerce")

        # --- Step 4: Handle missing values ---
        # Drop rows missing key ids (trip_id, start_time, end_time)
        self.trips = self.trips.dropna(subset=["trip_id", "start_time", "end_time"])
        # Fill missing duration/distance/capacity with median values
        self.trips["duration_minutes"] = self.trips["duration_minutes"].fillna(self.trips["duration_minutes"].median())
        self.trips["distance_km"] = self.trips["distance_km"].fillna(self.trips["distance_km"].median())
        self.stations["capacity"] = self.stations["capacity"].fillna(self.stations["capacity"].median())
        # Fill missing maintenance cost with 0
        self.maintenance["cost"] = self.maintenance["cost"].fillna(0)

        # --- Step 5: Remove invalid entries ---
        self.trips = self.trips[self.trips["end_time"] >= self.trips["start_time"]]

        # --- Step 6: Standardize categorical values ---
        self.trips["user_type"] = self.trips["user_type"].str.lower().str.strip()
        self.trips["status"] = self.trips["status"].str.lower().str.strip()
        self.maintenance["maintenance_type"] = self.maintenance["maintenance_type"].str.lower().str.strip()

        # Validate allowed values (if utils exists)
        try:
            from utils import VALID_USER_TYPES, VALID_BIKE_TYPES, VALID_MAINTENANCE_TYPES
            self.trips = self.trips[self.trips["user_type"].isin(VALID_USER_TYPES)]
            self.trips = self.trips[self.trips["bike_type"].isin(VALID_BIKE_TYPES)]
            self.maintenance = self.maintenance[self.maintenance["maintenance_type"].isin(VALID_MAINTENANCE_TYPES)]
        except ImportError:
            print("[Info] utils module not found; skipping allowed-values validation")

        # --- Step 7: Export cleaned data ---
        DATA_DIR.mkdir(exist_ok=True)
        self.trips.to_csv(DATA_DIR / "trips_clean.csv", index=False)
        self.stations.to_csv(DATA_DIR / "stations_clean.csv", index=False)
        self.maintenance.to_csv(DATA_DIR / "maintenance_clean.csv", index=False)

        print("[Step7] Cleaning complete. Cleaned CSVs saved to data/")

    # ------------------------------------------------------------------
    # Analytics — Business Questions
    # ------------------------------------------------------------------

    def total_trips_summary(self) -> dict:
        """Q1: Total trips, total distance, average duration.

        Returns:
            Dict with 'total_trips', 'total_distance_km', 'avg_duration_min'.
        """
        df = self.trips
        return {
            "total_trips": len(df),
            "total_distance_km": round(df["distance_km"].sum(), 2),
            "avg_duration_min": round(df["duration_minutes"].mean(), 2),
        }

    def top_start_stations(self, n: int = 10) -> pd.DataFrame:
        """Q2: Top *n* most popular start stations"""

        counts = self.trips["start_station_id"].value_counts().head(n).reset_index()
        counts.columns = ["station_id", "trip_count"]
        counts = counts.merge(
            self.stations[["station_id", "station_name"]], 
            on="station_id", 
            how="left"
        )
        return counts[["station_name", "trip_count"]]
    
    def peak_usage_hours(self) -> pd.Series:
        """Q3: Trip count by hour of day."""
        return self.trips["start_time"].dt.hour.value_counts().sort_index()

    def busiest_day_of_week(self) -> pd.Series:
        """Q4: Return the busiest day of the week and its number of trips as a pd.Series."""
        counts = self.trips["start_time"].dt.day_name().value_counts()
        busiest_day = counts.idxmax()
        trip_count = counts.max()
        return pd.Series({busiest_day: trip_count})


    def avg_distance_by_user_type(self) -> pd.Series:
        """Q5: Average trip distance grouped by user type."""
        return self.trips.groupby("user_type")["distance_km"].mean().round(2)

    def monthly_trip_trend(self) -> pd.Series:
        """Q7: Monthly trip counts over time."""
        return (
            self.trips
            .groupby(self.trips["start_time"].dt.to_period("M"))
            .size()
            .sort_index()
        )

    def top_active_users(self, n: int = 15) -> pd.DataFrame:
        """Q8: Top *n* most active users by trip count."""
        df = (self.trips.groupby("user_id", as_index=False).agg(total_trips=("trip_id", "count")))
        return df.sort_values("total_trips", ascending=False).head(n)
   
    def maintenance_cost_by_bike_type(self) -> pd.Series:
        """Q9: Total maintenance cost per bike type."""
        return (
            self.maintenance
            .groupby("bike_type")["cost"]
            .sum()
            .round(2)
        )

    def top_routes(self, n: int = 10) -> pd.DataFrame:
        """Q10: Most common start→end station pairs."""
        df = (
            self.trips
            .groupby(["start_station_id", "end_station_id"], as_index=False)
            .agg(trip_count=("trip_id", "count"))
            .sort_values("trip_count", ascending=False)
        )
        return df.head(n)

    # ------------------------------------------------------------------
    # Add more analytics methods here (Q6, Q11–Q14)
    # ------------------------------------------------------------------
    def bike_utilization_rate(self) -> pd.DataFrame:
        """Q6: Compute total usage duration per bike with bike type, sorted descending."""
        return (
            self.trips
            .groupby(['bike_id', 'bike_type'], as_index=False)['duration_minutes']
            .sum()
            .rename(columns={'duration_minutes': 'total_usage_min'})
            .sort_values('total_usage_min', ascending=False)
        )

    def is_peak_hour(self, hour: int) -> bool:
        return any(start <= hour <= end for start, end in self.PEAK_HOURS)

    def compute_fares(self):
        """Compute fares for all trips using vectorized NumPy and the pricing strategy classes."""
        trips = self.trips

        durations = trips["duration_minutes"].to_numpy()
        distances = trips["distance_km"].to_numpy()
        user_types = trips["user_type"].to_numpy()
        hours = trips["start_time"].dt.hour.to_numpy()

        fares = np.zeros(len(trips))

        # --- Casual pricing ---
        casual_mask = user_types == "casual"
        casual = CasualPricing()
        fares[casual_mask] = calculate_fares(
            durations=durations[casual_mask],
            distances=distances[casual_mask],
            per_minute=casual.PER_MINUTE,
            per_km=casual.PER_KM,
            unlock_fee=casual.UNLOCK_FEE,
        )

        # --- Member pricing ---
        member_mask = user_types == "member"
        member = MemberPricing()
        fares[member_mask] = calculate_fares(
            durations=durations[member_mask],
            distances=distances[member_mask],
            per_minute=member.PER_MINUTE,
            per_km=member.PER_KM,
            unlock_fee=0.0,
        )

        # --- Peak-hour surcharge ---
        peak_mask = np.zeros(len(trips), dtype=bool)
        for start, end in PEAK_HOURS:
            peak_mask |= (start <= hours) & (hours <= end)
        fares[peak_mask] *= PeakHourPricing.MULTIPLIER

        # --- Save fares ---
        self.trips["fare"] = np.round(fares, 2)


    def top_fares(self, n: int = 5) -> pd.DataFrame:
        """Return top n trips by fare."""
        return self.trips[["trip_id", "user_id", "fare"]].sort_values(
            "fare", ascending=False
        ).head(n)

    def avg_fare_by_user_type(self) -> pd.DataFrame:
        """Return average fare per user type."""
        return self.trips.groupby("user_type", as_index=False)["fare"].mean().round(2)


    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def generate_summary_report(self) -> None:
        """A summary text report to output/summary_report.txt."""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = OUTPUT_DIR / "summary_report.txt"

        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("  CityBike — Summary Report")
        lines.append("=" * 60)

        # --- Q1: Overall summary ---
        summary = self.total_trips_summary()
        lines.append("\n--- Overall Summary ---")
        lines.append(f"  Total trips       : {summary['total_trips']}")
        lines.append(f"  Total distance    : {summary['total_distance_km']} km")
        lines.append(f"  Avg duration      : {summary['avg_duration_min']} min")

        # --- Q2: Top start stations ---
        top_stations = self.top_start_stations()
        lines.append("\n--- Top 10 Start Stations ---")
        lines.append(top_stations.to_string(index=False))


        # --- Q3: Peak usage hours ---
        hours = self.peak_usage_hours()
        lines.append("\n--- Peak Usage Hours ---")
        lines.append(hours.to_string())

        # --- Q4: Busiest day of the week ---
        busiest_day = self.busiest_day_of_week()
        lines.append("\n--- Busiest Day of the Week ---")
        lines.append(busiest_day.to_string())

        # --- Q5: Average distance by user type ---
        avg_distance = self.avg_distance_by_user_type()
        lines.append("\n--- Average Distance by User Type ---")
        lines.append(avg_distance.to_string())

        # --- Q6: Monthly trip trend ---
        monthly_trend = self.monthly_trip_trend()
        lines.append("\n--- Monthly Trip Counts ---")
        lines.append(monthly_trend.to_string())

        # --- Q7: Top 15 Most Utilized Bikes ---
        top_bikes = self.bike_utilization_rate()
        lines.append("\n--- Top 10 Most Utilized Bikes ---")
        lines.append(top_bikes.head(10).to_string(index=False))

        # --- Q8: Top active users ---
        top_users = self.top_active_users()
        lines.append("\n--- Top 10 Active Users ---")
        lines.append(top_users.to_string(index=False))

        # --- Q9: Maintenance cost by bike type ---
        maint_cost = self.maintenance_cost_by_bike_type()
        lines.append("\n--- Maintenance Cost by Bike Type ---")
        lines.append(maint_cost.to_string(index=False))

        # --- Q10: Most common start→end station pairs ---
        top_routes = self.top_routes()
        lines.append("\n--- Top 10 Routes ---")
        lines.append(top_routes.to_string(index=False))


        # --- Fares Summary (NEW) ---
        lines.append("\n--- Fares Summary ---")
        if "fare" in self.trips.columns:
            total_revenue = self.trips["fare"].sum()
            lines.append(f"  Total revenue: €{total_revenue:.2f}")

            avg_fares = self.avg_fare_by_user_type()
            lines.append("\n  Average fare per user type:")
            lines.append(avg_fares.to_string(index=False))

            top5_fares = self.top_fares(n=5)
            lines.append("\n  Top 5 fares:")
            lines.append(top5_fares.to_string(index=False))
        else:
            lines.append("  Fares not computed yet. Run compute_fares() first.")

        report_text = "\n".join(lines) + "\n"
        report_path.write_text(report_text)
        
        print(f"Report saved to {report_path}")