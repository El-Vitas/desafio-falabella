#!/bin/sh
set -eu

python -m extraction.main

generated_dir=$(mktemp -d "$DATA_DIR/.generated.XXXXXX")
trap 'rm -rf "$generated_dir"' EXIT
python generator/generate_pokemon_data.py --out "$generated_dir" --pokemon-csv "$DATA_DIR/pokemon.csv"
for generated_file in "$generated_dir"/*.csv; do
    mv "$generated_file" "$DATA_DIR/"
done

folder_owner=$(stat -c %u "$DATA_DIR")
if ! find "$DATA_DIR" -maxdepth 1 -type f ! -uid "$folder_owner" -exec chown --reference="$DATA_DIR" {} +; then
    echo "WARNING: could not give the files in $DATA_DIR to the owner of the folder; the data itself is complete" >&2
fi
