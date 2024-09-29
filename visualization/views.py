from django.shortcuts import render
import dtmapi
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64


## I'll explain the steps in the below view fucntion with comments



def idp_visualization(request):
    # I use the below to Get IDP data for Ukraine by Oblast
    idp_data = dtmapi.get_idp_admin1_data(CountryName='Ukraine', to_pandas=True)

    # Here I Convert reportingDate to datetime format
    idp_data['reportingDate'] = pd.to_datetime(idp_data['reportingDate'])

    # I Now create charts for visualization
    plots = []
    
    # Chart 1: Total IDPs by Oblast over time
    total_idps_by_oblast = idp_data.groupby(['admin1Name', 'reportingDate'])['numPresentIdpInd'].sum().unstack().T
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    total_idps_by_oblast.plot(ax=ax1, title='Total IDPs by Oblast Over Time')
    ax1.set_xlabel('Reporting Date')
    ax1.set_ylabel('Number of IDPs')
    plots.append(encode_plot(fig1))

    # Chart 2: Latest IDP data by Oblast (tjis is a Bar chart)
    latest_date = idp_data['reportingDate'].max()
    latest_data = idp_data[idp_data['reportingDate'] == latest_date]
    
    # I now use the below to sort the data by IDPs count in ascending order
    latest_data_sorted = latest_data.groupby('admin1Name')['numPresentIdpInd'].sum().sort_values()

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    latest_data_sorted.plot(kind='bar', ax=ax2, title='IDPs by Oblast (Latest Data)', color='skyblue')
    ax2.set_xlabel('Oblast (Region)')
    ax2.set_ylabel('Number of IDPs')
    plots.append(encode_plot(fig2))

    # Chart 3: Change in IDPs over time for selected oblasts
    selected_oblasts = ['Kyivska', 'Lvivska', 'Donetska']  # Ensure these match the data
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    for oblast in selected_oblasts:
        subset = idp_data[idp_data['admin1Name'] == oblast]
        if not subset.empty:
            subset.plot(x='reportingDate', y='numPresentIdpInd', ax=ax3, label=oblast)
    ax3.set_title('Change in IDPs Over Time (Selected Oblasts)')
    ax3.set_xlabel('Reporting Date')
    ax3.set_ylabel('Number of IDPs')
    plots.append(encode_plot(fig3))

    context = {
        'plots': plots
    }
    
    return render(request, 'visualization/idp_visualization.html', context)

def encode_plot(fig):
    """Encode a matplotlib figure as a base64 string to embed in HTML."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return 'data:image/png;base64,' + string.decode('utf-8')
