import pandas as pd
import numpy as np
import glob
import os
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

def cargar_horas_efectivas(path):
    """
    Carga un archivo de la EPA y calcula la media ponderada de las horas efectivas (horase)
    para asalariados.
    """
    df = pd.read_csv(path, dtype=str)
    
    # Filtrar asalariados
    if 'situ' in df.columns:
        df['situ'] = df['situ'].str.strip().str.zfill(2)
        df_asalariados = df[df['situ'].isin(['07', '08'])].copy()
    elif 'situa' in df.columns:
        df['situa'] = df['situa'].str.strip().str.zfill(2)
        df_asalariados = df[df['situa'].isin(['07', '08'])].copy()
    else:
        df_asalariados = df.copy()

    # Factor de elevación
    if 'factorel' in df_asalariados.columns:
        df_asalariados['factorel'] = pd.to_numeric(df_asalariados['factorel'], errors='coerce') / 100.0
    else:
        df_asalariados['factorel'] = 1.0
        
    # Horas efectivas
    col_he = 'horase'
    if 'horase1' in df_asalariados.columns and 'horase' not in df_asalariados.columns:
        col_he = 'horase1'
        
    if col_he in df_asalariados.columns:
        df_asalariados[col_he] = pd.to_numeric(df_asalariados[col_he].str.strip(), errors='coerce').fillna(0)
    else:
        return np.nan
        
    # Media ponderada
    val = df_asalariados[col_he]
    wt = df_asalariados['factorel']
    media_he = (val * wt).sum() / wt.sum()
    
    return media_he

def main():
    base_dir = r"G:\Mi unidad\Proyectos\Impact_AI_creative_jobs\data\1_raw\epa\3digitos"
    # Tomamos desde 2018 hasta 2025
    archivos = sorted(glob.glob(os.path.join(base_dir, "EPA_20[1-2][0-9]T*.csv")))
    # Filtrar estrictamente >= 2018
    archivos = [a for a in archivos if int(os.path.basename(a).replace('EPA_', '')[:4]) >= 2018]
    
    datos_ts = []
    
    print("Calculando media de horas efectivas por trimestre (2018-2025)...")
    for path in archivos:
        filename = os.path.basename(path)
        year_str = filename.replace('EPA_', '')[:4]
        q_str = filename.replace('EPA_', '')[5:6]
        
        year = int(year_str)
        quarter = int(q_str)
        trimestre = f"{year}T{quarter}"
        
        media_he = cargar_horas_efectivas(path)
        
        if pd.notna(media_he):
            datos_ts.append({
                'Trimestre': trimestre,
                'Year': year,
                'Q': quarter,
                'Horas_Efectivas': media_he
            })
            print(f"{trimestre}: {media_he:.2f} hrs")

    df_ts = pd.DataFrame(datos_ts)
    df_ts = df_ts.sort_values(['Year', 'Q']).reset_index(drop=True)
    
    # Crear variables para el modelo RDiT
    df_ts['t'] = np.arange(1, len(df_ts) + 1)  # Tendencia temporal (1, 2, 3...)
    df_ts['Post_2021'] = (df_ts['Year'] >= 2021).astype(int)  # Salto por el cambio de cuestionario
    df_ts['Covid'] = ((df_ts['Year'] == 2020) & (df_ts['Q'] >= 2)).astype(int) | (df_ts['Year'] == 2021).astype(int) # Dummy simple para pandemia (impacto inicial)
    
    # Dummies estacionales
    df_ts['Q2'] = (df_ts['Q'] == 2).astype(int)
    df_ts['Q3'] = (df_ts['Q'] == 3).astype(int)
    df_ts['Q4'] = (df_ts['Q'] == 4).astype(int)

    # OLS: Horas_Efectivas ~ Tendencia + Post_2021 + Covid + Dummies Estacionales
    formula = "Horas_Efectivas ~ t + Post_2021 + Covid + Q2 + Q3 + Q4"
    modelo = smf.ols(formula, data=df_ts).fit()
    
    print("\n--- RESULTADOS DEL MODELO RDiT ---")
    print(modelo.summary())
    
    # Generar predicciones para gráfico
    df_ts['Prediccion'] = modelo.predict(df_ts)
    
    # Predicción contrafactual (qué habría pasado si Post_2021 fuera 0)
    df_cf = df_ts.copy()
    df_cf['Post_2021'] = 0
    df_ts['Contrafactual'] = modelo.predict(df_cf)
    
    # Gráfico
    img_dir = r"G:\Mi unidad\Proyectos\Substack\horas epa\imagenes"
    os.makedirs(img_dir, exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    # Serie original
    plt.plot(df_ts['Trimestre'], df_ts['Horas_Efectivas'], marker='o', color='black', label='Horas Efectivas (Observadas)', zorder=3)
    
    # Predicción del modelo
    plt.plot(df_ts['Trimestre'], df_ts['Prediccion'], linestyle='-', color='#d7191c', linewidth=2, label='Ajuste del Modelo', zorder=2)
    
    # Contrafactual
    # Dibujar la línea contrafactual solo a partir de 2021
    idx_post = df_ts[df_ts['Year'] >= 2021].index
    plt.plot(df_ts.loc[idx_post, 'Trimestre'], df_ts.loc[idx_post, 'Contrafactual'], linestyle='--', color='#2b83ba', linewidth=2, label='Contrafactual (sin cambio cuestionario)', zorder=2)
    
    # Marcar el cambio
    cambio_idx = df_ts[df_ts['Trimestre'] == '2021T1'].index[0]
    plt.axvline(x=cambio_idx - 0.5, color='gray', linestyle=':', label='Ruptura Metodológica (2021T1)')
    
    plt.title('Regresión Discontinua en el Tiempo: Efecto Cuestionario en Horas Efectivas', fontsize=14, pad=15)
    plt.xlabel('Trimestre', fontsize=12)
    plt.ylabel('Media Horas Efectivas Semanales', fontsize=12)
    plt.xticks(rotation=90)
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    img_path = os.path.join(img_dir, 'rdit_horas_efectivas.png')
    plt.savefig(img_path, dpi=300)
    print(f"\nFigura guardada en: {img_path}")

if __name__ == "__main__":
    main()
