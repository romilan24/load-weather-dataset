import pandas as pd

def import_data(load_dir, temp_dir):
    # Load data
    load = pd.read_csv(load_dir + 'hourly_caiso_load.csv')
    temp = pd.read_csv(temp_dir + 'combined_weather_data.csv')

    return load, temp

def merge_data(load, temp):
    # Merge dataframes on the datetime column
    merged_df = pd.merge(load, temp, how='inner', left_on='Time', right_on='Datetime')

    # Drop the duplicate 'Time' column
    merged_df = merged_df.drop('Datetime', axis=1)

    return merged_df

def swap_missing_data(merged_df, sf_columns, sj_columns):
    # Replace NaN values in San Francisco columns with values from San Jose columns
    for col_sf, col_sj in zip(sf_columns, sj_columns):
        merged_df[col_sf].fillna(merged_df[col_sj], inplace=True)
        merged_df[col_sj].fillna(merged_df[col_sf], inplace=True)

    return merged_df

def interpolate_missing_values(df, exclude_dates):
    """
    Interpolate missing values within each hour for numeric columns excluding specified dates.

    Parameters:
    - df: DataFrame containing the time series data.
    - exclude_dates: List of dates to exclude from interpolation.

    Returns:
    - DataFrame with NaN values replaced using linear interpolation within each hour.
    """

    result_df = df.copy()

    # Ensure 'Time' column is in datetime format
    result_df['Time'] = pd.to_datetime(result_df['Time'])

    # Exclude specified dates from interpolation
    for column in df.columns:
        if column not in ['Time', 'Current demand'] and pd.api.types.is_numeric_dtype(result_df[column]):
            try:
                # Convert the column to numeric (if not already)
                result_df[column] = pd.to_numeric(result_df[column], errors='coerce')

                # Extract hour component and interpolate within each hour
                result_df[column] = result_df.groupby(result_df['Time'].dt.hour)[column].transform(
                    lambda x: x.interpolate(method='linear', limit_direction='both'))

            except ValueError:
                print(f"Skipping interpolation for non-numeric column: {column}")

    return result_df

# Example usage
#update with local path to data after running weather-data-scrapper and caiso-load-downloader locally
load_dir = 'C:/Users/~/~/~/'
temp_dir = 'C:/Users/~/~/~/'

load, temp = import_data(load_dir, temp_dir)
merged_df = merge_data(load, temp)

# Swap missing data
sf_columns = [
    'KCASANFR698_Temperature', 'KCASANFR698_Dew_Point', 'KCASANFR698_Humidity',
    'KCASANFR698_Speed', 'KCASANFR698_Gust', 'KCASANFR698_Pressure']
sj_columns = [
    'KCASANJO17_Temperature', 'KCASANJO17_Dew_Point', 'KCASANJO17_Humidity',
    'KCASANJO17_Speed', 'KCASANJO17_Gust', 'KCASANJO17_Pressure']

merged_df = swap_missing_data(merged_df, sf_columns, sj_columns)

# Interpolate missing values
daylight_savings_dates = [pd.to_datetime('2021-03-14'), pd.to_datetime('2022-03-13'), pd.to_datetime('2023-03-12')]
merged_df = interpolate_missing_values(merged_df, daylight_savings_dates)
