import rasterio
import geopandas as gpd
from rasterstats import zonal_stats
import pandas as pd
from pathlib import Path

# --- Configuration ---
shapefile_path = r"D:\projects\tree-cover-jambi\batas_administrasi_jambi\batas_administasi_jambi.shp"
mitigasi_raster_path = r"D:\projects\tree-cover-jambi\raster\raster_tutupan.tif"

# Define the threshold for what constitutes "mitigation" from raster_tutupan.tif
# ADJUST THIS BASED ON WHAT YOUR PIXEL VALUES 0-19 ACTUALLY MEAN!
# Example: if values >= 10 represent 'high tree cover' or 'mitigation areas'
MITIGATION_VALUE_THRESHOLD = 10

# Pixel size for area calculation (assuming 30x30m for a 900 m2 pixel)
PIXEL_AREA_M2 = 900
M2_TO_HA = 10_000

# --- Load Data ---
print(f"Loading shapefile: {shapefile_path}")
try:
    gdf = gpd.read_file(shapefile_path)
    if 'nama_kec' not in gdf.columns:
        print("Warning: 'nama_kec' column not found in the shapefile. Please check your shapefile's attribute table for the correct sub-district name column.")
        print(f"Available columns: {gdf.columns.tolist()}")
        # You might need to manually set the correct column name here if it's different
        # For example, gdf['nama_kec'] = gdf['NAME_2'] if 'NAME_2' is the correct column
except Exception as e:
    print(f"Error loading shapefile: {e}")
    exit()

print(f"Loading mitigation raster: {mitigasi_raster_path}")
try:
    with rasterio.open(mitigasi_raster_path) as src:
        raster_nodata = src.nodata
        print(f"Raster NoData value detected: {raster_nodata}")
        print(f"Raster bounds: {src.bounds}")
        print(f"Raster CRS: {src.crs}")
except Exception as e:
    print(f"Error opening raster: {e}")
    exit()

# --- Define Custom Statistic for Mitigation ---
# This function will count pixels that meet your mitigation criteria
def count_mitigation_pixels(arr):
    """
    Counts pixels in the array that are considered 'mitigation' based on MITIGATION_VALUE_THRESHOLD.
    Also handles the raster's NoData value.
    """
    if raster_nodata is not None:
        # Exclude NoData pixels and count only those above the threshold
        return ((arr >= MITIGATION_VALUE_THRESHOLD) & (arr != raster_nodata)).sum()
    else:
        # If no NoData value is defined, just count above the threshold
        return (arr >= MITIGATION_VALUE_THRESHOLD).sum()

# --- Calculate Zonal Statistics ---
print("Calculating zonal statistics for mitigation...")
try:
    # Pass the GeoDataFrame directly to zonal_stats
    stats_mitigasi = zonal_stats(
        gdf,  # Vector input (your sub-district boundaries)
        mitigasi_raster_path, # Raster input (your mitigation data)
        add_stats={'mitigation_pixel_count': count_mitigation_pixels}, # Custom stat
        geojson_out=True, # Return GeoJSON-like output
        nodata=raster_nodata # Use the actual NoData value from the raster
    )
except Exception as e:
    print(f"Error during zonal_stats calculation: {e}")
    exit()


print("Processing results...")

# Convert list of features to GeoDataFrame
temp_mitigasi_gdf = gpd.GeoDataFrame.from_features(stats_mitigasi)

# Pastikan kolom mitigation_pixel_count ada
if 'mitigation_pixel_count' not in temp_mitigasi_gdf.columns:
    temp_mitigasi_gdf['mitigation_pixel_count'] = temp_mitigasi_gdf['properties'].apply(
        lambda x: x.get('mitigation_pixel_count', 0)
    )

# Gabungkan hasil ke GeoDataFrame asli
if len(gdf) == len(temp_mitigasi_gdf):
    gdf['mitigation_pixel_count'] = temp_mitigasi_gdf['mitigation_pixel_count'].values
else:
    print("Warning: jumlah fitur berbeda, menggabungkan berdasarkan index")
    gdf = gdf.reset_index(drop=True)
    temp_mitigasi_gdf = temp_mitigasi_gdf.reset_index(drop=True)
    gdf['mitigation_pixel_count'] = temp_mitigasi_gdf['mitigation_pixel_count'].fillna(0)

# Hitung luas mitigasi (hektar)
PIXEL_AREA_M2 = 900  # contoh 30m x 30m pixel
M2_TO_HA = 10000

gdf['luas_mitigasi_ha'] = gdf['mitigation_pixel_count'] * PIXEL_AREA_M2 / M2_TO_HA

# Buat folder output jika belum ada
output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)
output_csv_path = output_dir / "statistik_mitigasi_kecamatan.csv"

# Pilih kolom yang diinginkan dan rename
final_output_df = gdf[['NAME_2', 'luas_mitigasi_ha']].rename(columns={'NAME_2': 'nama_kec'})

if 'nama_kec' not in final_output_df.columns:
    print("Warning: Kolom 'nama_kec' tidak ditemukan, menyimpan hanya luas mitigasi")
    final_output_df = gdf[['luas_mitigasi_ha']]

try:
    final_output_df.to_csv(output_csv_path, index=False)
    print(f"Mitigation statistics saved successfully to {output_csv_path}")
except Exception as e:
    print(f"Error saving CSV: {e}")

print("Script finished.")
