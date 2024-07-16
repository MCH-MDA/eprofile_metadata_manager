# Script to create EUCOS formatted csv from instrument list
# Format as example in eprofile_config

# Begin with ALC example
import pandas as pd
import datetime

# Read the E-Profile meta-data from the hub
filename = '/home/sae/Documents/MetaData/eprofile-alc-instruments.csv'
df_alc = pd.read_csv(filename, sep=';')

# Read the instrument site file
df_sites = pd.read_csv('/home/sae/Documents/MetaData/eprofile-sites.csv', sep=';')

# For MeteoSwiss, only take valid rows with "Status==1"
#df = df[df['Status '] == 1]

# Create the EUCOS formatted csv
# Create the header
header = ['identifier', 'profile_id', 'Site_name', 'country code', 'latitude', 'longitude', 'observe', 'daily obs.']

# ISO country code list (country name capitalized)
country_codes = {
    'UK':'GBR',
    'SWITZERLAND': 'CHE',
    'FRANCE': 'FRA',
    'GERMANY': 'DEU',
    'AUSTRIA': 'AUT',
    'ITALY': 'ITA',
    'SPAIN': 'ESP',
    'PORTUGAL': 'PRT',
    'GREECE': 'GRC',
    'NORWAY': 'NOR',
    'SWEDEN': 'SWE',
    'FINLAND': 'FIN',
    'DENMARK': 'DNK',
    'NETHERLANDS': 'NLD',
    'BELGIUM': 'BEL',
    'LUXEMBOURG': 'LUX',
    'IRELAND': 'IRL',
    'UNITED KINGDOM': 'GBR',
    'ICELAND': 'ISL',
    'GREENLAND': 'GRL',
    'CANADA': 'CAN',
    'UNITED STATES': 'USA',
    'CYPRUS': 'CYP',
    'HUNGARY': 'HUN',
    'CZECH_REPUBLIC': 'CZE',
    'CROATIA': 'HRV',
    'SLOVENIA': 'SVN',
    'ROMANIA': 'ROU',
    'BULGARIA': 'BGR',
    'BRITISH OVERSEAS TERRITORY': 'GBR',
}

# For each row, create the EUCOS formatted csv
rows = []
for idx, row in df_alc.iterrows():
    # Read wigos from df_sites
    site_name = row['ccsi_name']
    site_row = df_sites[df_sites['ccsi_name'] == site_name]
    site_id = site_row['wigos'].values[0]
    identifier = site_id
    profile_id = row['eprofile_id']
    # Site name in eprofile instrument list is composed of both the name and country sep. by ","
    site_name = row['ccsi_name']
    country = site_row['country'].values[0]
    country_code = country_codes[country]
    latitude = site_row['ccsi_lat'].values[0]
    longitude = site_row['ccsi_lon'].values[0]
    observe = 1
    daily_obs = datetime.datetime.strptime(row['ccin_expected_reception_interval'], '%H:%M:%S') - datetime.datetime.strptime('00:00:00', '%H:%M:%S')
    # transform to seconds
    daily_obs = int(24*3600/daily_obs.total_seconds())

    # check if eprofile_gts is non empty:
    if not pd.isnull(row['eprofile_gts']):
        rows.append([identifier, profile_id, site_name, country_code, latitude, longitude, observe, daily_obs])
    else:
        print('E-Profile GTS is empty for site:', site_name)

# Create the dataframe
df_eucos = pd.DataFrame(rows, columns=header)
print(df_eucos)

# Write dataframe to csv file using "," as separator and following name convention: ALC_13_YYYYMMDD.csv where YYYYMMDD is the current date
date = datetime.datetime.now().strftime('%Y%m%d')
outfolder = '/home/sae/Documents/MetaData/'
filename = 'ALC_13_' + date + '.csv'
df_eucos.to_csv(outfolder+filename, sep=',', index=False)