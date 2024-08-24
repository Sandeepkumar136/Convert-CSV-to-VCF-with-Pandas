import pandas as pd

csv_file_path ="C:\\Users\\DELL\\Desktop\\Book Anal\\Booklet.csv"

df= pd.read_csv(csv_file_path)

def escape_vcf(text):
    return text.replace('\\', '\\\\').replace(';', '\\;').replace(',','\\,')


vcf_file_path='C:\\Users\\DELL\\Desktop\\Book Anal\\confile.vcf'

with open(vcf_file_path, 'w') as vcf_file:
    for _, row in df.iterrows():
        vcf_file.write('BEGIN:VCARD\n')
        vcf_file.write('VERSION:3.0\n')

        name = f"{escape_vcf(str(row['Family Name']))};{escape_vcf(str(row['Given Name']))};{escape_vcf(str(row['Additional Name']))};{escape_vcf(str(row['Name Prefix']))};{escape_vcf(str(row['Name Suffix']))}"
        vcf_file.write(f"N:{name}\n")
        vcf_file.write(f"FN:{escape_vcf(str(row['Name']))}\n")

        # Email fields
        if pd.notna(row['E-mail 1 - Value']):
            vcf_file.write(f"EMAIL;TYPE={escape_vcf(str(row['E-mail 1 - Type']))}:{escape_vcf(str(row['E-mail 1 - Value']))}\n")

        # Phone number fields
        phone_fields = ['Phone 1 - Value', 'Phone 2 - Value', 'Phone 3 - Value']
        phone_types = ['Phone 1 - Type', 'Phone 2 - Type', 'Phone 3 - Type']
        for phone_field, phone_type in zip(phone_fields, phone_types):
            if pd.notna(row[phone_field]):
                vcf_file.write(f"TEL;TYPE={escape_vcf(str(row[phone_type]))}:{escape_vcf(str(row[phone_field]))}\n")

        # Address fields
        if pd.notna(row['Address 1 - Formatted']):
            address = f"{escape_vcf(str(row['Address 1 - Street']))};{escape_vcf(str(row['Address 1 - City']))};{escape_vcf(str(row['Address 1 - Region']))};{escape_vcf(str(row['Address 1 - Postal Code']))};{escape_vcf(str(row['Address 1 - Country']))}"
            vcf_file.write(f"ADR;TYPE={escape_vcf(str(row['Address 1 - Type']))}:{address}\n")

        # Organization fields
        if pd.notna(row['Organization 1 - Name']):
            org = escape_vcf(str(row['Organization 1 - Name']))
            vcf_file.write(f"ORG:{org}\n")
            if pd.notna(row['Organization 1 - Department']):
                vcf_file.write(f"ORG:{escape_vcf(str(row['Organization 1 - Department']))}\n")
            if pd.notna(row['Organization 1 - Title']):
                vcf_file.write(f"TITLE:{escape_vcf(str(row['Organization 1 - Title']))}\n")

        # Website fields
        if pd.notna(row['Website 1 - Value']):
            vcf_file.write(f"URL:{escape_vcf(str(row['Website 1 - Value']))}\n")

        # Notes, if available
        if pd.notna(row['Notes']):
            vcf_file.write(f"NOTE:{escape_vcf(str(row['Notes']))}\n")

        vcf_file.write('END:VCARD\n')


print("VCF file created successfully")
