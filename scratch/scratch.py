'''
    pool = multiprocessing.Pool(25)
    


    logging.basicConfig()
    requests = computePowerAreaRequests(ee.FeatureCollection([ee.Feature(uk_adm2_all.first())]), power)
    areaPowers = pool.starmap(powerPerGeom, enumerate(requests))
    st.write(areaPowers)
    # try:
    # Page title
    #st.title("UK Renewables Table")

    # Read in county names
    constituencies = pd.read_csv("test_csv.csv")
    #st.write(print(constituencies))
    constituencies['Wind Energy Estimate (GW)'] = constituencies['sum']/1000 * 19.8 / 1000
    constituencies['Solar Energy Estimate (GW)'] = constituencies['sum']/1000 * 200 / 1000
    constituencies['Total Area Available for Devleopment (Km/2)'] = constituencies['sum']/1000 

    try:
        constituencies = constituencies.rename(columns = {"pcon19nm" : "Constituency"})
        #constituencies.set_index(constituencies['Constituency'])
        constituencies = constituencies[['Constituency', 'Wind Energy Estimate (GW)', 'Solar Energy Estimate (GW)', 'Total Area Available for Devleopment (Km/2)']]

    except:
        constituencies = constituencies.rename(columns = {"LAD21NM" : "Local Authority"})
        #constituencies.set_index(constituencies['Local Authority'])
        constituencies = constituencies[['Local Authority', 'Wind Energy Estimate (GW)', 'Solar Energy Estimate (GW)', 'Total Area Available for Devleopment (Km/2)']]



    # constituencies = constituencies["sum"]
    st.dataframe(constituencies)
    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csvDownload = convert_df(constituencies)
    st.download_button(
    "Download .csv",
    csvDownload,
    "Renewable Energy Potential.csv",
    "text/csv",
    key='download-csv1'   )
'''
