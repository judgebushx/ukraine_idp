import dtmapi
import pandas as pd


idp_data = dtmapi.get_idp_admin1_data(CountryName='Ukraine', to_pandas=True)


data_inspection = idp_data.head()


output_path = 'dtmapi_idp_data_inspection.xlsx'
with pd.ExcelWriter(output_path) as writer:
    data_inspection.to_excel(writer, sheet_name='IDP_Data', index=False)

print(f'Data exported to {output_path}')
