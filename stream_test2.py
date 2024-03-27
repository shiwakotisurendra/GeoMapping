import folium.raster_layers
import streamlit as st
import geopandas as gpd
import rasterio
import rasterio.plot
import matplotlib.pyplot as plt
import tempfile
import os
import folium
from streamlit_folium import folium_static
from rasterio.warp import calculate_default_transform, reproject, Resampling
# import leafmap.leafmap as leafmap

m= folium.plugins.DualMap(location=[50.9375, 6.9603], zoom_start=7)
marker_cluster = folium.plugins.MarkerCluster().add_to(m)
folium.plugins.Geocoder().add_to(m)
folium.plugins.MiniMap().add_to(m)
folium.LatLngPopup().add_to(m)
folium.plugins.MousePosition().add_to(m)
folium.plugins.Fullscreen().add_to(m)
folium.plugins.Terminator().add_to(m)

folium.plugins.LocateControl(auto_start=False).add_to(m)
folium.plugins.MeasureControl(
    position="topright",
    primary_length_unit="meters",
    secondary_length_unit="miles",
    primary_area_unit="sqmeters",
    secondary_area_unit="acres",
).add_to(m)
 # Enable drawing control
draw_plugin = folium.plugins.Draw(export=False, edit_options={"edit": True})
draw_plugin.add_to(m)
folium.TileLayer("CartoDB Voyager", show=False).add_to(m)

fg = folium.FeatureGroup(name="openseamap", overlay=True, control=True).add_to(m)

folium.TileLayer("CartoDB dark_matter", show=False).add_to(m)
folium.TileLayer(
    "https://tileserver.memomaps.de/tilegen/{z}/{x}/{y}.png",
    max_zoom=18,
    attr='Map <a href="https://memomaps.de/">memomaps.de</a> <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    name="PublicTransport",
    show=False,
).add_to(m)
folium.TileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles &copy; Esri &mdash; Source: USGS, Esri, TANA, DeLorme, and NPS",
    name="EsriWorldTerrain",
    max_zoom=13,
    show=False,
).add_to(m)
folium.TileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}",
    attr="ESRI NatGeoMap",
    name="ESRI NatGeoMap",
    show=False,
).add_to(m)
folium.TileLayer(
    "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
    name="OSMTopoMap",
    attr="Map data © OpenStreetMap contributors",
    show=False,
).add_to(m)
folium.TileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="ESRI Imagery",
    name="ESRI Imagery",
    show=True,
).add_to(m.m1)
folium.TileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="ESRI Imagery",
    name="ESRI Imagery",
    show=False,
).add_to(m.m2)
folium.TileLayer(
    "https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png",
    attr='<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    name="Cyle OSM",
    show=False,
).add_to(m)
folium.TileLayer(
    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}",
    max_zoom=20,
    attr='Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a>',
    name="USGS_Imagery",
    show=False,
).add_to(m)

folium.TileLayer(
    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}",
    max_zoom=20,
    attr='Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a>',
    name="USGS_TopoMap",
    show=False,
).add_to(m)
# folium.TileLayer("NASAGIBS Blue Marble").add_to(m)
# folium.TileLayer("OpenStreetMap",show=True).add_to(m)
folium.TileLayer(
    "http://tiles.openseamap.org/seamark/{z}/{x}/{y}.png",
    name="OpenSeaMap",
    attr="Map data © OpenSeaMap contributors",
).add_to(fg)
# m = leafmap.Map(location=[50.9375, 6.9603], zoom_start=4)

st.set_page_config(page_title="test dashboard",layout="wide")
def handle_upload(uploaded_file):

        if type(uploaded_file) == list and (
            any(".geojson" in file.name for file in uploaded_file)
            or any(".json" in file.name for file in uploaded_file)
        ):  # or any('.json' in file.name for file in uploaded_file)):
            # data = uploaded_file.read()
            for uploaded_file in uploaded_file:
                gdf = gpd.read_file(uploaded_file)
            
            return gdf

        elif type(uploaded_file) != list and (
            uploaded_file.name.endswith(".geojson")
            or uploaded_file.name.endswith(".json") 
            or uploaded_file.name.endswith(".gpkg")
        ):
            gdf = gpd.read_file(uploaded_file)
            return gdf

        elif any(".shp" in file.name for file in uploaded_file):

            with tempfile.TemporaryDirectory() as temp_dir:

                # Save the uploaded shapefile to a temporary directory
                for uploaded_file in uploaded_file:
                    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                    print(temp_file_path)
                    if uploaded_file.name.endswith(".shp"):
                        shp_path = temp_file_path
                    with open(temp_file_path, "wb") as temp_file:
                        temp_file.write(uploaded_file.getbuffer())

                gdf = gpd.read_file(shp_path)
            os.environ["SHAPE_RESTORE_SHX"] = "YES"

            print(shp_path)

            #############################################################################
            # with tempfile.TemporaryDirectory() as temp_dir:
            #     # Save the uploaded shapefile to a temporary directory
            #     # for ext in [".shp", ".shx", ".dbf", ".prj"]:
            #     temp_file_path = os.path.join(
            #         temp_dir, uploaded_file.name
            #     )
            #     with open(temp_file_path, "wb") as temp_file:
            #         temp_file.write(uploaded_file.getvalue())

            #     os.environ["SHAPE_RESTORE_SHX"] = "YES"
            #############################################################################

            print(gdf.head())
            # Assign a CRS to the GeoDataFrame if it is not already defined
            if gdf.crs is None:
                gdf.crs = "EPSG:4326"
            # Convert the shapefile to GeoJSON format
            gdf = gdf.to_crs("EPSG:4326")
            
            return gdf

# Function to upload vector data
def upload_vector():
    st.sidebar.subheader("Upload Vector Data:")
    uploaded_files = st.sidebar.file_uploader("Upload a shapefile", type=["geojson", "shx", "prj", "dbf", "shp", "json","gpkg"],accept_multiple_files=True,key="upload")
    if uploaded_files is not None:
        vector_data= handle_upload(uploaded_files)
        return vector_data

# Function to upload raster data
def upload_raster():
    st.sidebar.subheader("Upload Raster Data:")
    uploaded_file = st.sidebar.file_uploader("Upload a GeoTIFF", type=["tif", "tiff"])
    if uploaded_file is not None:
        # Define the target CRS (EPSG:4326 - WGS84)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(uploaded_file.getbuffer())
            dst_crs = 'EPSG:4326'
            try:
                with rasterio.open(temp_file_path) as src:
                    transform, width, height = calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds)

                    kwargs = src.meta.copy()
                    kwargs.update({
                        'crs': dst_crs,
                        'transform': transform,
                        'width': width,
                        'height': height
                    })

                    with rasterio.MemoryFile() as memfile:
                        with memfile.open(**kwargs) as dst:
                            for i in range(1, src.count + 1):
                                reproject(
                                    source=rasterio.band(src, i),
                                    destination=rasterio.band(dst, i),
                                    src_transform=src.transform,
                                    src_crs=src.crs,
                                    dst_transform=transform,
                                    dst_crs=dst_crs,
                                    resampling=Resampling.nearest
                                )

                            raster_data = dst.read(1)
                            bounds = dst.bounds

                            return raster_data, bounds
            except rasterio.errors.RasterioError as e:
                st.error(f"Error processing raster file: {e}")
                st.error("Please make sure the uploaded file is a valid GeoTIFF.")
                st.error("If the problem persists, contact support for assistance.")
                # Log the specific error message for debugging
                st.error(f"Error details: {e}")
                return None, None
    else:
        # Return None if no file is uploaded
        return None, None

# Function to display vector data
def display_vector(vector_data):
    st.subheader("Vector Data:")
    st.write(vector_data.head())
    gdf = vector_data
    if gdf.crs is None:
        gdf.crs = "EPSG:4326"
            # Convert the shapefile to GeoJSON format
        gdf = gdf.to_crs("EPSG:4326")
        
    def highlight_function(feature):
        return {
            "fillColor": "#ff0000",
            "color": "#000000",
            "weight": 1,
            "fillOpacity": 0.5,
        }
    if gdf.geometry.geom_type.unique() == 'Point':
        #  Add markers for each data point
        for index, row in gdf.iterrows():
            folium.Marker([row['geometry'].y, row['geometry'].x],popup=f"{dict(row[:-1])}").add_to(marker_cluster)
            # folium.LayerControl().add_to(m)
    # geojson_layer = folium.GeoJson(json.loads(geojson_data))
    
    else:
        jsond1 = folium.GeoJson(gdf, highlight_function=highlight_function).add_to(m.m1)
        folium.GeoJsonPopup(
            fields=[col for col in gdf.columns if col != "geometry"]
        ).add_to(jsond1)
        folium.GeoJsonTooltip(
            fields=[col for col in gdf.columns if col != "geometry"],
            style=(
                """background-color: grey; color: white; font-family:"
    courier new; font-size: 18px; padding: 5px;"""
            ),
        ).add_to(jsond1)
        jsond2 = folium.GeoJson(gdf, highlight_function=highlight_function).add_to(m.m2)
        folium.GeoJsonPopup(
            fields=[col for col in gdf.columns if col != "geometry"]
        ).add_to(jsond2)
        folium.GeoJsonTooltip(
            fields=[col for col in gdf.columns if col != "geometry"],
            style=(
                """background-color: grey; color: white; font-family:"
    courier new; font-size: 18px; padding: 5px;"""
            ),
        ).add_to(jsond2)
    
    
    
    

# Function to display raster data
def display_raster(raster_data,bounds):
    st.subheader("Raster Data:")
    # st.write(raster_data)
            # Create a colormap
    colormap = {
        '1.0': 'red',
        '0.0': 'white'
    }

    # # Create a Folium map centered at the mean latitude and longitude of the raster
    # center = [(bounds.bottom + bounds.top) / 2, (bounds.left + bounds.right) / 2]
    # m = folium.Map(location=center, zoom_start=10)

    # Add the raster overlay to the map
    folium.raster_layers.ImageOverlay(
        image=raster_data,
        bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
        colormap=colormap,opacity=0.5
    ).add_to(m.m1)
    
    folium.raster_layers.ImageOverlay(
        image=raster_data,
        bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
        colormap=colormap,opacity=0.5
    ).add_to(m.m2)
    


# Main function
def main():
    st.title("Geospatial Analysis Tool")

    # Upload vector data
    vector_data = upload_vector()
    if vector_data is not None:
        display_vector(vector_data)
        
        
    
    # Upload raster data
    raster_data,bounds = upload_raster()
    if raster_data is not None:
        display_raster(raster_data,bounds)
        # folium.raster_layers.WmsTileLayer(url="http://139.6.78.243/geoserver/geonode/wms?",layers="geonode:erft_bevoelkerungszahl",fmt= 'image/jpeg').add_to(m)
    folium.LayerControl().add_to(m)
    folium_static(m,width=1200,height=1100)

if __name__ == "__main__":
    main()
    
    
    
    
    
    
