import requests
import pandas as pd
import numpy as np
from itertools import combinations
from tqdm import tqdm


def get_osrm_roundtrip_edges(
    df,
    osrm_host="100.64.139.31",
    osrm_port=5000,
    profile="driving",
    node_id_col="node_id",
    lat_col="latitude",
    lon_col="longitude",
    block_size=50,
    timeout=300,
    weight_offset=1.0,
    save_path=None
):
    """
    Mengambil waktu tempuh antar node dari OSRM lokal
    dan menyimpan semua arah sebagai baris terpisah.

    Contoh:
    A -> B disimpan 1 baris
    B -> A disimpan 1 baris

    Output:
    - from_node
    - to_node
    - from_lat
    - from_lon
    - to_lat
    - to_lon
    - duration_sec
    - duration_min
    - distance_m
    - weight_inverse_time
    """

    required_cols = {node_id_col, lat_col, lon_col}
    missing_cols = required_cols - set(df.columns)

    if missing_cols:
        raise ValueError(f"Kolom berikut tidak ditemukan di df: {missing_cols}")

    nodes = (
        df[[node_id_col, lat_col, lon_col]]
        .dropna()
        .drop_duplicates(subset=[node_id_col])
        .reset_index(drop=True)
    )

    n = len(nodes)

    if n < 2:
        raise ValueError("Minimal harus ada 2 node.")

    node_ids = nodes[node_id_col].tolist()
    lats = nodes[lat_col].to_numpy()
    lons = nodes[lon_col].to_numpy()

    duration_matrix = np.full((n, n), np.nan, dtype=float)
    distance_matrix = np.full((n, n), np.nan, dtype=float)

    base_url = f"http://{osrm_host}:{osrm_port}/table/v1/{profile}"

    def coord_string(indices):
        """
        OSRM memakai format longitude,latitude.
        """
        return ";".join(
            f"{lons[i]},{lats[i]}"
            for i in indices
        )

    index_blocks = [
        list(range(start, min(start + block_size, n)))
        for start in range(0, n, block_size)
    ]

    for src_block in tqdm(index_blocks, desc="Mengambil data OSRM"):
        for dst_block in index_blocks:

            combined_indices = src_block + dst_block
            coords = coord_string(combined_indices)

            m = len(src_block)
            k = len(dst_block)

            sources = ";".join(str(i) for i in range(m))
            destinations = ";".join(str(i) for i in range(m, m + k))

            url = (
                f"{base_url}/{coords}"
                f"?sources={sources}"
                f"&destinations={destinations}"
                f"&annotations=duration,distance"
            )

            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
                data = response.json()

            except requests.exceptions.HTTPError as e:
                raise RuntimeError(
                    f"HTTP error dari OSRM.\n"
                    f"Status code: {response.status_code}\n"
                    f"Response: {response.text[:500]}\n"
                    f"URL awal: {url[:500]}..."
                ) from e

            except requests.exceptions.RequestException as e:
                raise RuntimeError(
                    f"Gagal menghubungi OSRM di {base_url}."
                ) from e

            if data.get("code") != "Ok":
                raise RuntimeError(f"OSRM error: {data}")

            durations = data.get("durations")
            distances = data.get("distances")

            if durations is None:
                raise RuntimeError("Response OSRM tidak memiliki field 'durations'.")

            durations = np.array(durations, dtype=float)

            if distances is not None:
                distances = np.array(distances, dtype=float)
            else:
                distances = np.full_like(durations, np.nan, dtype=float)

            for a, i in enumerate(src_block):
                for b, j in enumerate(dst_block):
                    duration_matrix[i, j] = durations[a, b]
                    distance_matrix[i, j] = distances[a, b]

    records = []

    for i in range(n):
        for j in range(n):

            if i == j:
                continue

            duration_sec = duration_matrix[i, j]
            distance_m = distance_matrix[i, j]

            if np.isnan(duration_sec):
                duration_min = np.nan
                weight_inverse_time = np.nan
            else:
                duration_min = duration_sec / 60
                weight_inverse_time = 1 / (duration_sec + weight_offset)

            records.append({
                "from_node": node_ids[i],
                "to_node": node_ids[j],
                "from_lat": lats[i],
                "from_lon": lons[i],
                "to_lat": lats[j],
                "to_lon": lons[j],
                "duration_sec": duration_sec,
                "duration_min": duration_min,
                "distance_m": distance_m,
                "weight_inverse_time": weight_inverse_time
            })

    edges_df = pd.DataFrame(records)

    if save_path is not None:
        if save_path.endswith(".parquet"):
            edges_df.to_parquet(save_path, index=False)
        elif save_path.endswith(".csv"):
            edges_df.to_csv(save_path, index=False)
        else:
            raise ValueError("Format save_path hanya mendukung .parquet atau .csv")

    return edges_df