import pandas as pd
import numpy as np
import glob
import os
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def cargar_y_limpiar(path):
    # Especificar dtype str para evitar problemas de tipos mixtos (y factor de elevación)
    df = pd.read_csv(path, dtype=str)
    
    # Filtrar asalariados: 'situ' == '07' (sector público) o '08' (sector privado)
    if 'situ' in df.columns:
        df['situ'] = df['situ'].str.strip().str.zfill(2)
        df_asalariados = df[df['situ'].isin(['07', '08'])].copy()
    elif 'situa' in df.columns:
        df['situa'] = df['situa'].str.strip().str.zfill(2)
        df_asalariados = df[df['situa'].isin(['07', '08'])].copy()
    else:
        df_asalariados = df.copy()

    # Estandarizar nombre de columna horash si viene como horash1
    if 'horash1' in df_asalariados.columns and 'horash' not in df_asalariados.columns:
        df_asalariados.rename(columns={'horash1': 'horash'}, inplace=True)

    # Convertir factor de elevación a float
    if 'factorel' in df_asalariados.columns:
        df_asalariados['factorel'] = pd.to_numeric(df_asalariados['factorel'], errors='coerce') / 100.0
    
    # Convertir horas a numérico (horash y horase)
    for col in ['horash', 'horase']:
        if col in df_asalariados.columns:
            df_asalariados[col] = pd.to_numeric(df_asalariados[col].str.strip(), errors='coerce').fillna(0)
            
    # Limpiar días de ausencia si existen (2021+)
    for col in ['dausvac', 'dausenf']:
        if col in df_asalariados.columns:
            df_asalariados[col] = pd.to_numeric(df_asalariados[col].str.strip(), errors='coerce').fillna(0)

    return df_asalariados

def procesar_trimestre_ej1(df):
    """
    Evaluar cuántas ausencias "desaparecerían" si aplicáramos 
    la lógica del cuestionario antiguo (solo preguntar si horase < horash).
    Retorna (total_ausentes, total_perdidos, dias_totales, dias_perdidos)
    """
    if 'dausvac' not in df.columns or 'dausenf' not in df.columns:
        return None

    df['ausencia_declarada'] = (df['dausvac'] > 0) | (df['dausenf'] > 0)
    total_ausentes = df[df['ausencia_declarada']]['factorel'].sum()
    
    df_perdidos = df[(df['ausencia_declarada']) & (df['horase'] >= df['horash'])]
    total_perdidos = df_perdidos['factorel'].sum()
    
    dias_totales = (df.loc[df['ausencia_declarada'], 'dausvac'] * df.loc[df['ausencia_declarada'], 'factorel']).sum() + \
                   (df.loc[df['ausencia_declarada'], 'dausenf'] * df.loc[df['ausencia_declarada'], 'factorel']).sum()
    
    dias_perdidos = (df_perdidos['dausvac'] * df_perdidos['factorel']).sum() + \
                    (df_perdidos['dausenf'] * df_perdidos['factorel']).sum()
                    
    return total_ausentes, total_perdidos, dias_totales, dias_perdidos

def main():
    base_dir = r"G:\Mi unidad\Proyectos\Impact_AI_creative_jobs\data\1_raw\epa\3digitos"
    # Buscar todos los archivos post 2021
    archivos = sorted(glob.glob(os.path.join(base_dir, "EPA_202[1-9]T*.csv")))
    
    resultados = []
    
    print("Iniciando procesamiento de trimestres post-2021...")
    for path in archivos:
        filename = os.path.basename(path)
        trimestre = filename.replace('EPA_', '').replace('.csv', '')
        
        df = cargar_y_limpiar(path)
        res = procesar_trimestre_ej1(df)
        
        if res:
            tot_aus, tot_per, dias_tot, dias_per = res
            if tot_aus > 0:
                pct_trab_perdidos = (tot_per / tot_aus) * 100
                pct_dias_perdidos = (dias_per / dias_tot) * 100
                
                resultados.append({
                    'Trimestre': trimestre,
                    'Asalariados_Ausentes': tot_aus,
                    'Trabajadores_Ocultos': tot_per,
                    'Pct_Trabajadores_Ocultos': pct_trab_perdidos,
                    'Dias_Ausencia_Totales': dias_tot,
                    'Dias_Ocultos': dias_per,
                    'Pct_Dias_Ocultos': pct_dias_perdidos
                })
                print(f"{trimestre}: {pct_trab_perdidos:.2f}% trab. ocultos | {pct_dias_perdidos:.2f}% días ocultos")

    df_res = pd.DataFrame(resultados)
    
    print("\n--- RESUMEN ESTADÍSTICO ---")
    print(df_res[['Pct_Trabajadores_Ocultos', 'Pct_Dias_Ocultos']].describe())
    
    # Prueba t para ver si la media es significativamente mayor que 0
    t_stat_trab, p_val_trab = stats.ttest_1samp(df_res['Pct_Trabajadores_Ocultos'], 0)
    t_stat_dias, p_val_dias = stats.ttest_1samp(df_res['Pct_Dias_Ocultos'], 0)
    
    print(f"\nSignificancia Estadística (H0: % Oculto = 0):")
    print(f"% Trabajadores Ocultos -> Media: {df_res['Pct_Trabajadores_Ocultos'].mean():.2f}% | p-valor: {p_val_trab:.4e}")
    print(f"% Días Ocultos         -> Media: {df_res['Pct_Dias_Ocultos'].mean():.2f}% | p-valor: {p_val_dias:.4e}")

    # Generar y guardar figura
    img_dir = r"G:\Mi unidad\Proyectos\Substack\horas epa\imagenes"
    os.makedirs(img_dir, exist_ok=True)
    
    # Ordenar por trimestre para asegurar cronología correcta en el gráfico
    df_res = df_res.sort_values('Trimestre')
    
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    
    plt.plot(df_res['Trimestre'], df_res['Pct_Trabajadores_Ocultos'], marker='o', color='#2b83ba', label='% Trabajadores Ocultos')
    plt.plot(df_res['Trimestre'], df_res['Pct_Dias_Ocultos'], marker='s', color='#d7191c', label='% Días Ocultos')
    
    plt.title('Efecto del Cuestionario EPA: Ausencias Ocultas (Simulación post-2021)', fontsize=14, pad=15)
    plt.xlabel('Trimestre', fontsize=12)
    plt.ylabel('Porcentaje Oculto (%)', fontsize=12)
    plt.xticks(rotation=45)
    plt.axhline(0, color='black', linewidth=1)
    
    # Añadir valores medios como líneas punteadas
    plt.axhline(df_res['Pct_Trabajadores_Ocultos'].mean(), color='#2b83ba', linestyle='--', alpha=0.5)
    plt.axhline(df_res['Pct_Dias_Ocultos'].mean(), color='#d7191c', linestyle='--', alpha=0.5)
    
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    img_path = os.path.join(img_dir, 'ausencias_ocultas.png')
    plt.savefig(img_path, dpi=300)
    print(f"\nFigura guardada en: {img_path}")

if __name__ == "__main__":
    main()
