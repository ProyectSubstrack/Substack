# Substack Graphics Skill & Guidelines

Esta es la instrucción o "skill" oficial para la generación de gráficos en los proyectos de la carpeta `/Substack`. Cuando se te pida generar o modificar gráficos (mediante Python/Matplotlib/Seaborn), debes cumplir OBLIGATORIAMENTE con las siguientes reglas:

## 1. Identidad Visual (Marca)
Todos los gráficos deben mantener una estética monocromática elegante, basada en tonos crema, terracota, marrones y rojos ladrillo. DEBES inyectar y utilizar el siguiente bloque de configuración en tus scripts o notebooks:

```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    'figure.facecolor': '#FDFBF7', # Crema suave
    'axes.facecolor': '#FAF6F0',   # Crema más oscuro
    'axes.edgecolor': '#E3DCD2',   # Marrón muy claro
    'axes.labelcolor': '#4A3B32',  # Marrón oscuro
    'text.color': '#4A3B32',
    'xtick.color': '#4A3B32',
    'ytick.color': '#4A3B32',
    'grid.color': '#E3DCD2',
    'grid.linestyle': '--',
    'grid.alpha': 0.7,
    'legend.facecolor': '#FAF6F0',
    'legend.edgecolor': '#E3DCD2',
    'font.family': 'sans-serif'
})

BRAND_COLORS = {
    'primary': '#A33327',   # Rojo ladrillo profundo
    'secondary': '#D47B5A', # Terracota cálido
    'tertiary': '#C68B59',  # Ámbar/arcilla
    'quaternary': '#E3ACA1',# Rojo pastel apagado
    'highlight': '#5C2317', # Marrón/rojo muy oscuro
    'muted': '#A49080'      # Marrón grisáceo tenue
}
```
*   Usa los colores del diccionario `BRAND_COLORS` para líneas, barras y marcadores.
*   Para colormaps (Heatmaps, etc.), utiliza el mapa secuencial cálido `OrRd` de matplotlib.

## 2. Generación Bilingüe
Todo gráfico generado debe producirse SIEMPRE POR DUPLICADO:
1.  Versión en Español (idioma principal).
2.  Versión en Inglés.

## 3. Nombrado de Archivos
*   Versión en español: `[nombre_del_grafico].png` (ej. `analisis_completo.png`).
*   Versión en inglés: DEBE llevar el sufijo `_eng`, es decir, `[nombre_del_grafico]_eng.png` (ej. `analisis_completo_eng.png`).

## 4. Directorio de Destino
*   **Todos** los gráficos generados (ambas versiones) deben guardarse OBLIGATORIAMENTE dentro del subdirectorio `imagenes/` correspondiente al proyecto actual (ej. `/Substack/[Nombre_del_Proyecto]/imagenes/`).
*   Si el directorio `imagenes/` no existe, tu código debe crearlo automáticamente (`os.makedirs('imagenes', exist_ok=True)`).
