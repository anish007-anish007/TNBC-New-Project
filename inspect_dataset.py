import gzip

path = "data/raw/GSE31519_TNBC_SampleInfo_BCR.txt.gz"

with gzip.open(path, "rt", encoding="utf-8") as file:
    rows = [line.rstrip("\r\n").split("\t") for line in file]

for field_name in ["SampleNames", "Array_type", "GSM_accession", "Biopsy_Method"]:
    row = next(row for row in rows if row[0].strip() == field_name)

    print("\n", field_name)
    print("First 6 values:", row[1:7])