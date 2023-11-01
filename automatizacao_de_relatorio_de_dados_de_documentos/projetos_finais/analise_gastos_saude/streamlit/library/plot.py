import pandas as pd


def get_metodo_analitico(rema_df: pd.DataFrame, plot=False) -> pd.DataFrame:
    ylabel= 'Métodos Analíticos'
    _df = (
        rema_df.reset_index()
            .melt(id_vars=["index"], value_vars=rema_df.columns[6:22],var_name = ylabel)
            .query('value == True')
            .loc[:, ylabel]
            .value_counts(ascending=True)            
    )
    
    if plot:
        return _df.plot(kind='barh')
    
    return _df