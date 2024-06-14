def main():
    world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres')
    )


if __name__ == "__main__":
    main()
