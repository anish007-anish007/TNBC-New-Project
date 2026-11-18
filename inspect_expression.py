
import gzip
import pandas as pd

metadata_path = "data/raw/GSE31519_TNBC_SampleInfo_BCR.txt.gz"
expression_path = "data/raw/GSE31519_complete_dataset.txt.gz"

# Read metadata
metadata = pd.read_csv(
    metadata_path,
    sep="\t",
    dtype=str,
    header=None
)

metadata_samples = metadata.iloc[0, 1:].tolist()

# Read expression header information
with gzip.open(expression_path, "rt") as file:
    lines = [next(file) for _ in range(4)]

expression_samples = lines[1].rstrip("\r\n").split("\t")
expression_arrays = lines[2].rstrip("\r\n").split("\t")
expression_gsm = lines[3].rstrip("\r\n").split("\t")

# Identify populated sample columns
valid_columns = [
    i for i in range(1, len(expression_samples))
    if expression_samples[i].strip()
]

expression_sample_names = [
    expression_samples[i].strip()
    for i in valid_columns
]

# Compare metadata and expression sample names
metadata_set = set(metadata_samples)
expression_set = set(expression_sample_names)

missing = sorted(metadata_set - expression_set)
extra = sorted(expression_set - metadata_set)

print("METADATA SAMPLE COUNT:", len(metadata_samples))
print("UNIQUE METADATA SAMPLES:", len(metadata_set))
print("EXPRESSION SAMPLE COUNT:", len(expression_sample_names))
print("UNIQUE EXPRESSION SAMPLES:", len(expression_set))

print("\nMISSING FROM EXPRESSION:", missing)
print("EXTRA IN EXPRESSION:", extra)

print("\nDUPLICATE EXPRESSION SAMPLE NAMES:")
duplicates = pd.Series(expression_sample_names)
print(duplicates[duplicates.duplicated()].tolist())

print("\nARRAYEXPRESS SAMPLE COUNT:")
print(sum(
    "ArrayExpress" in expression_arrays[i]
    for i in valid_columns
))
