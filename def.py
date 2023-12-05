import pandas as pd

def calidad_datos(data):
    tipos = pd.DataFrame({'tipo': data.dtypes}, index=data.columns)
    na = pd.DataFrame({'nulos': data.isna().sum()}, index=data.columns)
    
    na_prop = pd.DataFrame({'prop_nulos': data.isna().mean()}, index=data.columns)
    
    ceros = pd.DataFrame({
        'ceros': [data[col].eq(0).sum() for col in data.columns],
        'prop_ceros': [data[col].eq(0).mean() for col in data.columns]
    }, index=data.columns)
    
    ceros_prop = pd.DataFrame({'prop_ceros': (data == 0).mean()}, index=data.columns)
    
    summary = data.describe(include='all').T

    summary['dist_IQR'] = summary['75%'] - summary['25%']
    summary['limit_inf'] = summary['25%'] - summary['dist_IQR']*1.5
    summary['limit_sup'] = summary['75%'] + summary['dist_IQR']*1.5

    summary['outlier'] = data.apply(lambda x: np.sum((x < summary.loc[x.name, 'limit_inf']) | (x > summary.loc[x.name, 'limit_sup'])), axis=1)


    return pd.concat([tipos, na, na_prop, ceros, ceros_prop, summary[['mean', 'std', 'min', '25%', '50%', '75%', 'max', 'dist_IQR', 'limit_inf', 'limit_sup', 'outlier']]], axis=1).sort_values(by='prop_ceros', ascending=False)