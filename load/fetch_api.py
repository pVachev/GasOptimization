import pandas as pd
from entsog import EntsogPandasClient

from datetime import date
import meteostat as ms

client = EntsogPandasClient()

start_gas = pd.Timestamp('20210102', tz='Europe/Brussels')
end_gas = pd.Timestamp('20260101', tz='Europe/Brussels')
country_code = "LU"  # Luxembourg


gas_df = client.query_aggregated_data(start = start_gas, end = end_gas, country_code = country_code)


start_temp = date(2020, 1, 2)
end_temp = date(2025, 12, 31)

# Get daily data

ts = ms.daily(ms.Station(id='06590'), start_temp, end_temp)
temp_df = ts.fetch()

temp_df = temp_df["temp"]



gas_f = gas_df.loc[(gas_df["points_names"].str.contains("Public Distribution"))
                      & (gas_df["indicator"] == "Allocation") 
                      & (gas_df["direction_key"] == "exit")
]

cols = ["day", "month", "year"]
gas_f['date'] = gas_f[cols].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)

# gas_f.set_index("date", inplace=True)

gas_f["date"] = pd.to_datetime(gas_f["date"], format = "%d-%m-%Y")

gas_f.set_index("date", inplace=True)

print(gas_f)
print(temp_df)
