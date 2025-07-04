import geopandas as gpd
import pandas as pd
import folium

# Load shapefile kabupaten
gdf = gpd.read_file(r"D:\projects\tree-cover-jambi\batas_administrasi_jambi\batas_administasi_jambi.shp")

# Rename kolom agar konsisten
gdf = gdf.rename(columns={"NAME_2": "nama_kec"})

# Load CSV
df = pd.read_csv("output/statistik_mitigasi_kecamatan.csv")

# Merge
merged = gdf.merge(df, on="nama_kec")

# Inisialisasi peta
m = folium.Map(location=[-1.5, 102], zoom_start=7)

# Tambahkan choropleth
folium.Choropleth(
    geo_data=merged,
    data=merged,
    columns=["nama_kec", "luas_mitigasi_ha"],
    key_on="feature.properties.nama_kec",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Total Kehilangan Tutupan Pohon (ha)"
).add_to(m)

# Tambahkan label dan popup
for _, row in merged.iterrows():
    # Hitung centroid polygon
    centroid = row.geometry.centroid
    nama = row['nama_kec']
    luas = row['luas_mitigasi_ha']

    # Tambahkan tooltip + marker
    folium.Marker(
        location=[centroid.y, centroid.x],
        icon=folium.DivIcon(html=f"""
            <div style="font-size: 10pt; color: black; font-weight: bold; text-shadow: 1px 1px 1px white;">
                {nama}
            </div>"""),
        popup=folium.Popup(f"{nama}: {luas:.2f} ha", max_width=200)
    ).add_to(m)

# Simpan
m.save("output/peta_deforestasi_total.html")
print("Peta berhasil disimpan ke output/peta_deforestasi_total.html")
