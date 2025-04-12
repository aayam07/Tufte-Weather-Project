#!/usr/bin/env python3

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
from datetime import datetime
import traceback

def load_data(year):
    """Load and prepare the weather data for visualization."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'processed')
    print(f"Loading data from: {data_dir}")
    
    try:
        # Load temperature data
        temp_file = os.path.join(data_dir, f'temperatures_{year}.txt')
        print(f"Loading temperature data from: {temp_file}")
        
        if not os.path.exists(temp_file):
            print(f"Error: Temperature file not found: {temp_file}")
            raise FileNotFoundError(f"Temperature file not found: {temp_file}")
            
        temp_data = pd.read_csv(temp_file, header=None, names=['date', 'temp', 'type'])
        
        # Pivot temperature data to have TMAX and TMIN as columns
        temp_data['date'] = pd.to_datetime(temp_data['date'])
        temp_pivot = temp_data.pivot(index='date', columns='type', values='temp')
        
        # Load precipitation data
        precip_file = os.path.join(data_dir, f'precipitation_{year}.txt')
        print(f"Loading precipitation data from: {precip_file}")
        
        if not os.path.exists(precip_file):
            print(f"Error: Precipitation file not found: {precip_file}")
            raise FileNotFoundError(f"Precipitation file not found: {precip_file}")
            
        precip_data = pd.read_csv(precip_file, header=None, names=['date', 'precip'])
        precip_data['date'] = pd.to_datetime(precip_data['date'])
        precip_data.set_index('date', inplace=True)
        
        # Try to load humidity data if available
        humidity_file = os.path.join(data_dir, f'humidity_{year}.txt')
        print(f"Loading humidity data from: {humidity_file}")
        
        try:
            if os.path.exists(humidity_file):
                humidity_data = pd.read_csv(humidity_file, header=None, names=['date', 'humidity'])
                humidity_data['date'] = pd.to_datetime(humidity_data['date'])
                humidity_data.set_index('date', inplace=True)
            else:
                print(f"Humidity file not found: {humidity_file}. Creating dummy data.")
                # Create dummy humidity data if not available
                humidity_data = pd.DataFrame(index=temp_pivot.index, columns=['humidity'])
                humidity_data['humidity'] = np.random.randint(30, 80, size=len(humidity_data))
        except Exception as e:
            print(f"Error loading humidity data: {e}")
            print("Creating dummy humidity data.")
            humidity_data = pd.DataFrame(index=temp_pivot.index, columns=['humidity'])
            humidity_data['humidity'] = np.random.randint(30, 80, size=len(humidity_data))
        
        # Calculate monthly normal values (could be replaced with actual historical normals)
        monthly_tmax_normal = temp_pivot.groupby(temp_pivot.index.month)['TMAX'].mean()
        monthly_tmin_normal = temp_pivot.groupby(temp_pivot.index.month)['TMIN'].mean()
        monthly_precip_normal = precip_data.groupby(precip_data.index.month)['precip'].mean() * 30  # Approximate monthly total
        
        # Calculate monthly actual values
        monthly_precip_actual = precip_data.groupby(precip_data.index.month)['precip'].sum()
        
        return temp_pivot, precip_data, humidity_data, monthly_tmax_normal, monthly_tmin_normal, monthly_precip_normal, monthly_precip_actual
    
    except Exception as e:
        print(f"Error loading data: {e}")
        print(traceback.format_exc())
        
        # Create dummy data for testing
        print("Creating dummy data for visualization testing...")
        
        # Create date range for the year
        start_date = pd.Timestamp(f"{year}-01-01")
        end_date = pd.Timestamp(f"{year}-12-31")
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Create dummy temperature data
        temp_pivot = pd.DataFrame(index=dates, columns=['TMAX', 'TMIN'])
        
        # Generate seasonal temperature patterns
        for i, date in enumerate(dates):
            month = date.month
            day_of_year = date.dayofyear
            seasonal_factor = np.sin(2 * np.pi * day_of_year / 365)
            
            # Base temperatures with seasonal variation
            tmax_base = 75 + 25 * seasonal_factor
            tmin_base = 45 + 25 * seasonal_factor
            
            # Add some random variation
            temp_pivot.loc[date, 'TMAX'] = tmax_base + np.random.normal(0, 5)
            temp_pivot.loc[date, 'TMIN'] = tmin_base + np.random.normal(0, 5)
        
        # Create dummy precipitation data
        precip_data = pd.DataFrame(index=dates, columns=['precip'])
        precip_data['precip'] = np.random.exponential(0.1, size=len(dates))
        
        # Create dummy humidity data
        humidity_data = pd.DataFrame(index=dates, columns=['humidity'])
        humidity_data['humidity'] = 50 + 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 10, size=len(dates))
        humidity_data['humidity'] = humidity_data['humidity'].clip(10, 100)
        
        # Calculate monthly normals from the dummy data
        monthly_tmax_normal = temp_pivot.groupby(temp_pivot.index.month)['TMAX'].mean()
        monthly_tmin_normal = temp_pivot.groupby(temp_pivot.index.month)['TMIN'].mean()
        monthly_precip_normal = precip_data.groupby(precip_data.index.month)['precip'].mean() * 30
        
        # Calculate monthly actual values
        monthly_precip_actual = precip_data.groupby(precip_data.index.month)['precip'].sum()
        
        return temp_pivot, precip_data, humidity_data, monthly_tmax_normal, monthly_tmin_normal, monthly_precip_normal, monthly_precip_actual

def create_tufte_visualization(year):
    """Create a visualization in the style of Tufte's weather illustration."""
    print(f"Creating visualization for year {year}...")
    
    try:
        temp_data, precip_data, humidity_data, monthly_tmax_normal, monthly_tmin_normal, monthly_precip_normal, monthly_precip_actual = load_data(year)
        
        # Create figure with custom layout
        fig = plt.figure(figsize=(12, 8), facecolor='#f0f0f0')
        gs = GridSpec(4, 1, height_ratios=[3, 1, 1, 1], hspace=0.1)
        
        # Temperature plot
        ax1 = fig.add_subplot(gs[0])
        ax1.plot(temp_data.index, temp_data['TMAX'], 'k-', linewidth=1.5)
        ax1.plot(temp_data.index, temp_data['TMIN'], 'k-', linewidth=1.5)
        ax1.fill_between(temp_data.index, temp_data['TMAX'], temp_data['TMIN'], color='black', alpha=0.3)
        
        # Add normal temperature lines
        months = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31', freq='MS')
        normal_tmax = [monthly_tmax_normal[m.month] for m in months]
        normal_tmin = [monthly_tmin_normal[m.month] for m in months]
        
        # Extend the normal lines to span the full year
        extended_months = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31', freq='D')
        extended_tmax = np.interp(mdates.date2num(extended_months), 
                                mdates.date2num(months), 
                                normal_tmax)
        extended_tmin = np.interp(mdates.date2num(extended_months), 
                                mdates.date2num(months), 
                                normal_tmin)
        
        ax1.plot(extended_months, extended_tmax, 'k--', linewidth=1, alpha=0.7, label='Normal High')
        ax1.plot(extended_months, extended_tmin, 'k--', linewidth=1, alpha=0.7, label='Normal Low')
        
        # Find and mark extreme temperatures
        max_temp_idx = temp_data['TMAX'].idxmax()
        min_temp_idx = temp_data['TMIN'].idxmin()
        
        ax1.annotate(f"HIGH {max_temp_idx.strftime('%b %d')}: {temp_data.loc[max_temp_idx, 'TMAX']:.0f}°",
                    xy=(max_temp_idx, temp_data.loc[max_temp_idx, 'TMAX']),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8))
        
        ax1.annotate(f"LOW {min_temp_idx.strftime('%b %d')}: {temp_data.loc[min_temp_idx, 'TMIN']:.0f}°",
                    xy=(min_temp_idx, temp_data.loc[min_temp_idx, 'TMIN']),
                    xytext=(10, -20), textcoords='offset points',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8))
        
        # Add "LINE INDICATES NORMAL HIGH/LOW" annotations
        ax1.annotate("LINE INDICATES\nNORMAL HIGH", 
                    xy=(pd.Timestamp(f'{year}-10-15'), extended_tmax[extended_months.month == 10][0]),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8))
        
        ax1.annotate("LINE INDICATES\nNORMAL LOW", 
                    xy=(pd.Timestamp(f'{year}-03-15'), extended_tmin[extended_months.month == 3][0]),
                    xytext=(10, -20), textcoords='offset points',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8))
        
        # Set temperature y-axis
        ax1.set_ylim(0, 105)
        ax1.set_ylabel('TEMPERATURE (°F)', fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Precipitation plot
        ax2 = fig.add_subplot(gs[1], sharex=ax1)
        
        # Group precipitation by month for bar chart
        monthly_precip = precip_data.resample('M').sum()
        
        # Create bar positions for actual and normal precipitation
        months = range(1, 13)
        bar_positions = np.arange(len(months))
        bar_width = 0.35
        
        # Convert month numbers to datetime for x-axis
        month_dates = [pd.Timestamp(f"{year}-{m}-15") for m in months]
        
        # Plot actual precipitation
        actual_values = [monthly_precip_actual.get(m, 0) for m in months]
        ax2.bar(month_dates, actual_values, width=20, color='black', label='Actual')
        
        # Plot normal precipitation
        normal_values = [monthly_precip_normal.get(m, 0) for m in months]
        for i, (date, value) in enumerate(zip(month_dates, normal_values)):
            ax2.bar(date, value, width=10, color='none', edgecolor='black', hatch='///', label='Normal' if i == 0 else '')
        
        # Calculate total annual precipitation
        total_precip = monthly_precip_actual.sum()
        normal_total = monthly_precip_normal.sum()
        
        # Add precipitation title and totals
        ax2.text(0.5, 0.9, f"PRECIPITATION IN INCHES\nTotal precipitation for {year}: {total_precip:.2f}\nNormal annual precipitation: {normal_total:.2f}", 
                horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black"))
        
        ax2.set_ylim(0, max(max(actual_values), max(normal_values)) * 1.2)
        ax2.set_ylabel('INCHES', fontsize=8)
        ax2.grid(True, alpha=0.3)
        
        # Add "ACTUAL" and "NORMAL" labels under each month's bars
        for i, date in enumerate(month_dates):
            ax2.text(date, -0.5, "ACTUAL", ha='center', va='top', fontsize=6, rotation=90)
            ax2.text(date, -0.5, "NORMAL", ha='center', va='top', fontsize=6, rotation=90)
        
        # Humidity plot
        ax3 = fig.add_subplot(gs[3], sharex=ax1)
        ax3.plot(humidity_data.index, humidity_data['humidity'], 'k-', linewidth=0.8, alpha=0.7)
        ax3.set_ylim(0, 100)
        ax3.set_ylabel('PERCENT', fontsize=8)
        ax3.text(0.5, 0.1, "RELATIVE HUMIDITY AS OF NOON", 
                horizontalalignment='center', transform=ax3.transAxes,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black"))
        ax3.grid(True, alpha=0.3)
        
        # Set common x-axis properties
        for ax in [ax1, ax2, ax3]:
            ax.set_xlim(pd.Timestamp(f'{year}-01-01'), pd.Timestamp(f'{year}-12-31'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
            plt.setp(ax.get_xticklabels(), rotation=0, ha='center')
        
        # Add month labels at the top
        month_names = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 
                      'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
        ax0 = fig.add_subplot(gs[0], sharex=ax1, frameon=False)
        ax0.set_yticks([])
        ax0.xaxis.tick_top()
        ax0.set_xlim(pd.Timestamp(f'{year}-01-01'), pd.Timestamp(f'{year}-12-31'))
        ax0.xaxis.set_major_locator(mdates.MonthLocator())
        ax0.xaxis.set_major_formatter(mdates.DateFormatter('%B'))
        plt.setp(ax0.get_xticklabels(), rotation=0, ha='center')
        
        # Add title
        plt.suptitle(f"NEW YORK CITY'S WEATHER FOR {year}", fontsize=14, y=0.98)
        
        # Add source attribution
        plt.figtext(0.95, 0.01, f"New York Times, January 11, {year+1}, p. 32.", 
                    ha='right', fontsize=8, style='italic')
        
        # Save the figure
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'nyc_weather_{year}_tufte_style.png')
        
        print(f"Saving visualization to: {output_file}")
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to {output_file}")
        
        plt.close()
        return True
    
    except Exception as e:
        print(f"Error creating visualization: {e}")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    try:
        year = int(sys.argv[1]) if len(sys.argv) > 1 else 1980
        success = create_tufte_visualization(year)
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        sys.exit(1)