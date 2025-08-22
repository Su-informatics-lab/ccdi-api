import pandas as pd
import csv
import sys
import logging

def load_mapping(sheet):
    mapping = {}
    for _, row in sheet.iterrows():
        ipo_col = row['Column']
        ccdi_col = row['CCDI Column']
        value_mappings = str(row['IPO-to-CCDI Value Mapping']).split(',')

        value_map = {}
        any_to_any = False
        for vm in value_mappings:
            vm = vm.strip()
            if '->' in vm:
                ipo_val, ccdi_val = map(str.strip, vm.split('->'))
                if ipo_val == 'Any' and ccdi_val == 'Any':
                    any_to_any = True
                else:
                    value_map[ipo_val] = ccdi_val

        mapping[ipo_col] = {
            'ccdi_col': ccdi_col,
            'value_map': value_map,
            'any_to_any': any_to_any
        }
    return mapping

def translate_row(row, mapping):
    translated = {}
    for ipo_col, value in row.items():
        if ipo_col not in mapping:
            logging.warning(f"Column '{ipo_col}' not found in mapping. Skipping")
            continue

        map_info = mapping[ipo_col]
        ccdi_col = map_info['ccdi_col']
        value_map = map_info['value_map']
        any_to_any = map_info['any_to_any']

        # Sometimes race and ethnicity are provided as a semicolon-separated list,
        # in those cases take the first value.
        if (ipo_col in ['race', 'ethnicity']):
            split_value = value.split(';')
            value = split_value[0].strip()
            if len(split_value) > 1:
                logging.info(f"Splitting colon-separated value {value} in column '{ipo_col}'")
        

        if ipo_col in ['age_at_vital_status'] and pd.isna(value):
            translated[ccdi_col] = '0'
        elif value in value_map:
            translated[ccdi_col] = value_map[value]
        elif any_to_any:
            translated[ccdi_col] = value
        else:
            logging.warning(f"No mapping found for value '{value}' in column '{ipo_col}', and no 'Any -> Any' fallback. Row:\n{row}")
            translated[ccdi_col] = ''
    return translated

def main():
    if len(sys.argv) != 5:
        print("Usage: python ipo_to_ccdi_translator.py <IPO_schemas.xlsx> <subjects|samples|files> <input_ipo.csv> <output_ccdi.csv>")
        sys.exit(1)

    excel_file = sys.argv[1]
    tab_name = sys.argv[2]
    input_csv = sys.argv[3]
    output_csv = sys.argv[4]

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    logging.info("Loading mapping from Excel file...")

    if tab_name not in ['subjects', 'samples', 'files']:
        logging.error(f"Invalid tab name '{tab_name}'. Must be one of 'subjects', 'samples', or 'files'.")
        sys.exit(1)

    tab_name = tab_name + '.csv'

    schema_df = pd.read_excel(excel_file, sheet_name=tab_name, engine='openpyxl')
    mapping = load_mapping(schema_df)

    logging.info("Reading input IPO CSV file...")
    ipo_data = pd.read_csv(input_csv)

    logging.info("Translating IPO data to CCDI format...")
    translated_data = [translate_row(row, mapping) for _, row in ipo_data.iterrows()]

    logging.info("Writing output CCDI CSV file...")
    if translated_data:
        ccdi_df = pd.DataFrame(translated_data)
        ccdi_df.to_csv(output_csv, index=False)
    else:
        logging.warning("No data to write to output file.")

    logging.info("Translation complete.")

if __name__ == "__main__":
    main()

