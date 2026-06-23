import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns

def cargar_y_limpiar(path):
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
        
    # Estandarizar
    if 'horash1' in df_asalariados.columns and 'horash' not in df_asalariados.columns:
        df_asalariados.rename(columns={'horash1': 'horash'}, inplace=True)
    if 'horase1' in df_asalariados.columns and 'horase' not in df_asalariados.columns:
        df_asalariados.rename(columns={'horase1': 'horase'}, inplace=True)
    
    for col in ['horash', 'horase']:
        if col in df_asalariados.columns:
            df_asalariados[col] = pd.to_numeric(df_asalariados[col].str.strip(), errors='coerce').fillna(0) / 100.0
            
    return df_asalariados

def procesar_ano(year, base_dir):
    archivos = glob.glob(os.path.join(base_dir, f"EPA_{year}T*.csv"))
    dfs = []
    for path in archivos:
        df = cargar_y_limpiar(path)
        dfs.append(df)
        
    if not dfs: return None
    df_year = pd.concat(dfs, ignore_index=True)
    
    # Calcular diferencia de horas (Horas Perdidas)
    df_year['horas_perdidas'] = df_year['horash'] - df_year['horase']
    
    # Solo nos interesan los que efectivamente trabajaron menos de lo habitual (horas_perdidas > 0)
    df_ausentes = df_year[df_year['horas_perdidas'] > 0].copy()
    
    # Agrupar por tramos de horas perdidas
    bins = [0, 4, 8, 16, 30, np.inf]
    labels = ['1-4 hrs\n(Medio día/Micro)', '5-8 hrs\n(1 día)', '9-16 hrs\n(2 días)', '17-30 hrs\n(3-4 días)', '31+ hrs\n(Semana completa)']
    
    df_ausentes['tramo'] = pd.cut(df_ausentes['horas_perdidas'], bins=bins, labels=labels)
    
    # Sumar factor de elevación por tramo para obtener volumen poblacional
    distribucion = df_ausentes.groupby('tramo')['factorel'].sum()
    
    # Calcular porcentaje del total de ausencias para ver el "peso" relativo de los pequeños olvidos
    porcentaje = (distribucion / distribucion.sum()) * 100
    
    # Queremos devolver el volumen medio trimestral para que sea comparable
    volumen_trimestral = distribucion / len(archivos)
    
    return pd.DataFrame({'Volumen_Medio': volumen_trimestral, 'Porcentaje': porcentaje})

def main():
    base_dir = r"G:\Mi unidad\Proyectos\Impact_AI_creative_jobs\data\1_raw\epa\3digitos"
    
    print("Analizando distribución de ausencias en 2019 (Pre-cambio)...")
    df_2019 = procesar_ano(2019, base_dir)
    
    print("Analizando distribución de ausencias en 2023 (Post-cambio)...")
    # Evitamos 2020 y 2021 por el ruido de la pandemia pura y el ERTE
    df_2023 = procesar_ano(2023, base_dir)
    
    df_2019['Periodo'] = '2019 (Cuestionario Antiguo)'
    df_2023['Periodo'] = '2023 (Nuevo Cuestionario)'
    
    df_plot = pd.concat([df_2019.reset_index(), df_2023.reset_index()])
    
    print("\n--- VOLUMEN MEDIO TRIMESTRAL POR TRAMO ---")
    pivot_vol = df_plot.pivot(index='tramo', columns='Periodo', values='Volumen_Medio')
    pivot_vol['Crecimiento (%)'] = ((pivot_vol['2023 (Nuevo Cuestionario)'] / pivot_vol['2019 (Cuestionario Antiguo)']) - 1) * 100
    print(pivot_vol)
    
    # Directorio de salida para la prensa
    out_dir = r"G:\Mi unidad\Proyectos\Substack\horas epa\docx"
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Guardar CSV
    csv_path = os.path.join(out_dir, 'datos_distribucion_ausencias.csv')
    # Renombrar columnas para el CSV final
    csv_out = pivot_vol.copy()
    csv_out.index.name = "Tramos de Horas de Ausencia"
    csv_out.columns = ["Volumen Medio Trimestral 2019", "Volumen Medio Trimestral 2023", "Crecimiento (%)"]
    
    # Añadir fuente en el CSV (como un comentario al principio o final, o dejarlo limpio)
    with open(csv_path, 'w', encoding='utf-8-sig') as f:
        f.write("Título: El Efecto Olvido - Explosión de Ausencias Cortas (2019 vs 2023)\n")
        f.write("Fuente: Encuesta de Población Activa (EPA), INE. Elaboración propia.\n\n")
    csv_out.to_csv(csv_path, mode='a', sep=';', decimal=',')
    
    # 2. Guardar Gráfico
    plt.figure(figsize=(12, 6.5))
    sns.set_style("whitegrid")
    
    sns.barplot(data=df_plot, x='tramo', y='Volumen_Medio', hue='Periodo', palette=['#2b83ba', '#d7191c'])
    
    plt.title('El "Efecto Olvido": Explosión de Ausencias Cortas (2019 vs 2023)', fontsize=16, pad=20, fontweight='bold')
    plt.xlabel('Volumen de Horas Ausentes en la Semana', fontsize=12)
    plt.ylabel('Volumen Medio Trimestral (Trabajadores)', fontsize=12)
    plt.legend(title='', fontsize=11)
    
    # Fuente
    plt.figtext(0.99, 0.01, 'Fuente: Encuesta de Población Activa (EPA), INE. Elaboración propia.', 
                horizontalalignment='right', fontsize=10, color='gray', style='italic')
    
    # Formatear el eje Y
    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)).replace(',', '.')))
    
    plt.tight_layout(rect=[0, 0.05, 1, 1]) # Dejar espacio para la fuente
    
    img_path = os.path.join(out_dir, 'distribucion_ausencias_prensa.png')
    plt.savefig(img_path, dpi=300, bbox_inches='tight')
    print(f"\nCSV y Figura guardados en: {out_dir}")

if __name__ == "__main__":
    main()
