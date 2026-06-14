# Modelo Neoclásico Dinámico de dos sectores y dos países con efecto Balassa-Samuelson

Este documento resume la estructura del modelo desarrollado y presenta un ejercicio teórico-cuantitativo (transición determinista de previsión perfecta) para evaluar la evolución de la brecha de bienestar entre ambas economías.

---

## 1. Fundamentos y Estructura del Modelo

El modelo consta de dos economías interdependientes, $D$ (Dinámico) y $S$ (Social). Ambas cuentan con 4 sectores institucionales que interactúan en un entorno dinámico e intertemporal con acumulación de capital y política fiscal:

### 1.1 Familias (Households)
Las familias maximizan su utilidad intertemporal:
$$\max \sum_{t=0}^{\infty} \beta^t \left( \frac{C_t^{1-\sigma}}{1-\sigma} - \chi \frac{L_t^{1+\varphi}}{1+\varphi} \right)$$

Sujeto a la restricción presupuestaria:
$$P_t^C C_t + P_t^I I_t + B_{t+1} + P_t^C T_t = W_t L_t + R_t K_t + (1+r_t) B_t$$

Y la ley de movimiento del capital:
$$K_{t+1} = (1-\delta) K_t + I_t$$

**Condiciones de Primer Orden (FOCs):**
1. **Oferta Laboral**: $\chi L_t^\varphi = C_t^{-\sigma} \frac{W_t}{P_t^C}$
2. **Ecuación de Euler (Bonos)**: $C_t^{-\sigma} = \beta \mathbb{E}_t \left[ C_{t+1}^{-\sigma} \frac{P_t^C}{P_{t+1}^C} (1+r_{t+1}) \right]$
3. **Ecuación de Euler (Capital)**: $1 = \beta \mathbb{E}_t \left[ \left( \frac{C_{t+1}}{C_t} \right)^{-\sigma} \left( \frac{R_{t+1}}{P_{t+1}^C} + 1 - \delta \right) \right]$ (Asumiendo $P^I = P^C$ para simplificar).

### 1.2 Empresas (Firms)
Hay libre movilidad de capital y trabajo entre sectores dentro de un país.

**Sector Tecnológico (Transable, T)**
$$Y_{T,t} = A_{T,t} K_{T,t}^\alpha L_{T,t}^{1-\alpha}$$
FOCs (Precio igual a costo marginal):
*   $R_t = P_{T,t} \alpha \frac{Y_{T,t}}{K_{T,t}}$
*   $W_t = P_{T,t} (1-\alpha) \frac{Y_{T,t}}{L_{T,t}}$

**Sector Social (No Transable, N)**
$$Y_{N,t} = A_{N,t} K_{N,t}^\eta L_{N,t}^{1-\eta}$$
FOCs:
*   $R_t = P_{N,t} \eta \frac{Y_{N,t}}{K_{N,t}}$
*   $W_t = P_{N,t} (1-\eta) \frac{Y_{N,t}}{L_{N,t}}$

### 1.3 Gobierno y Política Fiscal
El gobierno recauda impuestos de suma fija $T_t$, consume bienes $G_t$ y emite deuda $D_t$.
$$P_t^C G_t + (1+r_t) D_t = P_t^C T_t + D_{t+1}$$

### 1.4 Comercio, Agregadores y Tipo de Cambio Real
En este modelo existen cuatro bienes producidos en total (el bien transable y el no transable de cada país). Sin embargo, los consumidores de cada país demandan un agregado de **tres bienes** específicos: su bien no transable local y un compuesto de los dos bienes transables (el doméstico y el importado).

La demanda final total $Q_{i,t} = C_{i,t} + I_{i,t} + G_{i,t}$ del país $i$ es un agregado CES de la cesta de bienes transables ($T$) y el bien no transable local ($N$):
$$Q_{i,t} = \left[ \gamma^{\frac{1}{\phi}} (Q_{T,i,t})^{\frac{\phi-1}{\phi}} + (1-\gamma)^{\frac{1}{\phi}} (Q_{N,i,t})^{\frac{\phi-1}{\phi}} \right]^{\frac{\phi}{\phi-1}}$$

A su vez, la cesta de bienes transables se forma mediante un **agregador Armington** que combina el bien transable doméstico (producido en $i$) y el bien transable importado (producido en $j$):
$$Q_{T,i,t} = \left[ \omega^{\frac{1}{\theta}} (Q_{T,ii,t})^{\frac{\theta-1}{\theta}} + (1-\omega)^{\frac{1}{\theta}} (Q_{T,ji,t})^{\frac{\theta-1}{\theta}} \right]^{\frac{\theta}{\theta-1}}$$

Esto da lugar a un índice de precios para el agregado transable $P_{T,i,t}^{agg}$ en cada país:
$$P_{T,i,t}^{agg} = \left[ \omega (P_{T,i,t})^{1-\theta} + (1-\omega) (P_{T,j,t})^{1-\theta} \right]^{\frac{1}{1-\theta}}$$

Y finalmente, el Índice de Precios al Consumidor (IPC) general para el país $i$:
$$P_{i,t}^C = \left[ \gamma (P_{T,i,t}^{agg})^{1-\phi} + (1-\gamma) P_{N,i,t}^{1-\phi} \right]^{\frac{1}{1-\phi}}$$

El **Tipo de Cambio Real (TCR)** se define como la ratio de los índices de precios al consumidor entre ambos países:
$$TCR = \frac{P_S^C}{P_D^C}$$

### Mecanismo Clave: Efecto Balassa-Samuelson
El núcleo del modelo asume que el país Dinámico ($D$) experimenta un alto crecimiento en su productividad tecnológica ($A_{T,D}$), mientras que el país Social ($S$) mantiene una enorme ventaja en la eficiencia de su sector de servicios sociales ($A_{N,S} \gg A_{N,D}$).

---

## 2. Ejercicio de Evaluación Cuantitativa

El objetivo de este ejercicio es evaluar de forma integral cómo evoluciona la economía a lo largo del tiempo bajo distintos ritmos de innovación. Simulamos una transición de 50 periodos (ej. años) donde la tecnología de ambos países crece, pero a ritmos asimétricos: la productividad transable del país Dinámico ($A_{T,D}$) crece al 2% por periodo, mientras que la del país Social ($A_{T,S}$) crece al 1%. Al mismo tiempo, mantenemos fijas las productividades del sector social de cada país.

![Análisis Completo de Resultados](./analisis_completo.png)

### 2.1. Evolución de Productividades en el Tiempo
Para lograr un escenario más realista y observar el efecto Balassa-Samuelson en estado puro, hemos modificado la calibración asumiendo que los servicios locales en D son el doble de ineficientes que en S ($A_{N,D}=1.0, A_{N,S}=2.0$). Además, hemos asignado un peso muy fuerte a los servicios no transables en la cesta de consumo (70%), lo cual es la norma en las economías modernas. 

**Importante (Lo Asumido vs. Lo Derivado):** El ranking absoluto de bienestar y consumo (S por encima de D en niveles) no lo genera el efecto Balassa-Samuelson per se, sino que queda fijado en $t=0$ por la calibración de eficiencias. En $t=0$, con igual tecnología ($A_{T,D}=A_{T,S}=1$), el país S ya consume un ~64% más en términos reales ($C_S/C_D \approx 1.64$, o equivalentemente D está un 39% por debajo de S). El resultado Balassa-Samuelson genuino del modelo es **dinámico**: pese a que la tecnología de D casi se triplica en 50 periodos, el boom tecnológico no logra cerrar esta brecha, pasando D de estar un ~39% por debajo a un ~27% por debajo.

### 2.2. Evolución de Salarios Nominales y Reales
A medida que $D$ experimenta el boom tecnológico, la rentabilidad marginal del trabajo en el sector $T$ se dispara, lo que arrastra los salarios nominales ($W_D$) fuertemente al alza. Por el contrario, el salario nominal en el país $S$ ($W_S$) parece caer. Sin embargo, esto es un artefacto de usar el IPC de D como numerario ($P_D^C = 1$). Si observamos la línea punteada naranja (Salario Real de S, $W_S / P_S^C$), el poder adquisitivo de los salarios en S de hecho se mantiene estable o sube, inducido por la mayor demanda de exportaciones y el abaratamiento de los transables. Nominalmente, D se vuelve un país extremadamente "caro", pero no necesariamente más rico en poder de compra local. 

### 2.3. Brecha de Consumo Real y Términos de Intercambio
Si mirásemos solo los salarios nominales, esperaríamos que el consumo real de $D$ aplastase al de $S$. Sin embargo, la **brecha de consumo real es mucho más estrecha que la nominal**. Además, observamos que el consumo de S cae muy levemente a lo largo del tiempo. Esto es un efecto de **términos de intercambio**: al abaratarse masivamente el bien transable de D, la exportación relativa de S pierde valor en el mercado internacional, perjudicando su nivel de consumo general.

¿Por qué D no logra adelantar a S en consumo real? (Efecto Balassa-Samuelson): Los altos salarios en $D$ encarecen brutalmente el precio de sus bienes no transables, erosionando el poder adquisitivo real de sus familias. *Caveat*: Hay que notar que los menores precios $P_{N,S}$ reflejan en parte menores salarios en el sector servicios de S, y el modelo no ajusta por la calidad de estos servicios; por tanto "más barato" no equivale mecánicamente a "más eficiente", aunque operativamente deflacte el consumo.

### 2.4. Evolución del Bienestar (CEV) y Horas Trabajadas
Para evaluar de forma estricta quién está mejor, utilizamos la **Variación Equivalente en Consumo (CEV)**: el % de consumo extra por periodo que necesitaría D para igualar el bienestar intertemporal exacto de S. Esta métrica es superior al simple consumo real porque penaliza el esfuerzo laboral (las horas trabajadas).

El cuadrante inferior derecho muestra dos fenómenos reveladores. Por un lado, las familias en D trabajan sustancialmente más horas ($L_D > L_S$) a lo largo de toda la transición. Por otro, la **CEV se mantiene altamente positiva**: en $t=0$, D necesitaría un 75% más de consumo para alcanzar la felicidad de S. En $t=50$, tras medio siglo de explosión tecnológica, la CEV cae al 47%. D recorta terreno, pero el incesante trabajo y la inflación de servicios impiden que el boom tecnológico cierre por completo la brecha de bienestar subyacente. 

### 2.5. Evolución de los Precios y Tipo de Cambio Real
Para entender a fondo la dinámica del poder adquisitivo, resulta crucial observar qué sucede con los precios a nivel desagregado y cómo componen el Índice de Precios al Consumidor ($P^C$). Recordemos que en el modelo, el deflactor de consumo para el país $D$ se utiliza como numeraire ($P_D^C = 1$).

![Evolución de los Precios](./evolucion_precios.png)

Como se aprecia en la nueva figura:
1. **Panel Izquierdo (Bienes No Transables):** El precio del bien no transable en el país Dinámico ($P_{N,D}$) crece vertiginosamente a lo largo del tiempo. Esto se debe a los altos salarios nominales que debe pagar para competir con el sector tecnológico (efecto Balassa-Samuelson), combinados con su menor eficiencia en este sector. En el país Social, el precio de los servicios locales ($P_{N,S}$) crece muy lentamente.
2. **Panel Central (Cesta Transable - Agregado Armington):** Los índices de precios del agregado transable para ambos países ($P_{T,D}^{agg}$ y $P_{T,S}^{agg}$) caen fuertemente. Esto ocurre porque el incesante progreso tecnológico (especialmente en $D$) abarata sistemáticamente el costo de producción de la cesta transable para el mundo entero. 
3. **Panel Derecho (Índice de Precios al Consumidor, IPC):** El deflactor general muestra cómo se compensan estas fuerzas. En $D$, el abaratamiento de la cesta transable se contrarresta exactamente con el encarecimiento extremo de los servicios locales para mantener $P_D^C = 1$. En contraste, en el país $S$, como los servicios locales casi no se encarecen y los bienes transables importados se vuelven más baratos, su coste de vida general ($P_S^C$) experimenta una fuerte caída estructural. 

Dado que el Tipo de Cambio Real ($TCR$) equivale a $P_S^C / P_D^C$, y $P_D^C = 1$, la curva morada ($P_S^C$) representa simultáneamente el TCR. Esta fuerte caída significa que **el país Dinámico se encarece en términos relativos (apreciación real)**. El país $D$ se vuelve extremadamente "caro", explicando por qué sus altos salarios no logran cerrar la brecha de bienestar real.

### 2.6. Análisis de Sensibilidad (Mecanismo vs Supuesto)
Para hacer transparente qué parte del bienestar viene determinada por supuestos estructurales frente a mecanismos de precios, hemos generado un mapa de calor (Heatmap) que evalúa la CEV en $t=50$ variando el peso de los servicios ($1-\gamma$) y la ventaja de eficiencia social ($A_{N,S}/A_{N,D}$).

![Heatmap de Sensibilidad](./heatmap.png)

Como muestra el mapa, si el peso de los servicios cae o si las eficiencias se igualan ($A_{N,S}/A_{N,D} \to 1$), la CEV se vuelve negativa (D supera a S en bienestar, zona verde). La tesis "Krugman/Social" requiere indefectiblemente que los servicios no transables pesen enormemente en la vida moderna y que el país S sea genuinamente más eficiente (zona roja/amarilla).

### Conclusión Principal
Incluso con una brecha de eficiencia en servicios mucho más realista y moderada, el país dinámico sufre una "penalización de ineficiencia relativa" que erosiona buena parte de los frutos de su avance tecnológico. El país social, a través del comercio internacional y la eficiencia en la provisión de servicios locales esenciales, no solo amortigua el shock de quedarse atrás tecnológicamente, sino que logra sostener un nivel de bienestar estrictamente superior al de su vecino super-tecnológico.

---

## 3. Síntesis y Gráfico de Cierre (Crecimiento Relativo)

Para condensar toda la narrativa macroeconómica, el siguiente gráfico muestra la evolución en **tasas de crecimiento** de las principales variables, **normalizadas a 1 en el periodo inicial**. Esto no mide "quién es más rico" (nivel absoluto), sino "quién crece más rápido" a partir de $t=0$.

![Gráfico de Cierre](./grafico_cierre.png)

*   **Panel 1 (Productividad Tecnológica Exógena):** Muestra el verdadero "motor" del modelo ($A_{T,D}$ vs $A_{T,S}$). Se observa cómo la tecnología en el país D se dispara espectacularmente a lo largo de las décadas frente a S. ¡Una brecha gigantesca se abre!
*   **Panel 2 (Salarios Nominales):** Es el canal de transmisión primario. Los salarios en $D$ explotan nominalmente para retener a los trabajadores en el sector tecnológico, mientras que en $S$ crecen a un ritmo mucho más modesto.
*   **Panel 3 (Consumo Nominal):** Las familias de $D$, con sus abultados salarios, gastan nominalmente muchísimo más que las de $S$. Si solo mirásemos el dinero gastado, $D$ parecería aplastar a $S$.
*   **Panel 4 (Consumo Real):** El golpe de realidad y la demostración pura del **Efecto Balassa-Samuelson**. A pesar de que la productividad tecnológica (Panel 1) y el gasto en dinero (Panel 3) abrieron brechas colosales a favor de D, al deflactar por los altísimos precios de sus ineficientes servicios locales, el crecimiento del consumo real de D se desploma. La brecha de consumo real crece menos de la mitad de lo que creció la brecha tecnológica. Toda esa supuesta "ventaja productiva" se evaporó en inflación interna.

---

## 4. Brechas Relativas (Ratios D/S)

Para visualizar aún más claro el "espejismo" de las tasas de crecimiento, podemos graficar el ratio directo entre las tasas de avance del país D y el país S, **normalizando todas las líneas a 1.0 en el periodo inicial**. Esto nos permite comparar visualmente el "terreno relativo recortado" independientemente del punto de partida.

![Gráfico de Ratios](./ratios.png)

1.  **Productividad Tecnológica ($A_T$):** La línea azul puntuada se dispara sin freno, llegando a ser casi un 65% superior en D.
2.  **Salarios y Consumo Nominal:** La línea morada y roja (que viajan pegadas) suben aún más fuerte que la tecnología. Esto es lo que vemos si medimos la economía usando el tipo de cambio de mercado internacional: Estados Unidos aplastando económicamente a Europa.
3.  **Consumo Real (Paridad de Poder Adquisitivo):** La línea verde gruesa revela la verdadera brecha en el bienestar de los ciudadanos dentro de sus fronteras. Gracias a los servicios eficientes de Europa y los encarecidos en EE. UU., la línea verde se mantiene casi plana (apenas crece un 19% a favor de D en medio siglo). **La colosal ventaja tecnológica no se transforma en una mejora de vida equivalente**.

---

## 5. Corolario Final: ¿Quién tiene razón, Krugman o Garicano?

A la luz de este modelo DSGE calibrado con el Efecto Balassa-Samuelson, podemos concluir de forma salomónica que en el intenso debate económico actual, **tanto Luis Garicano (y los defensores de la tesis del declive) como Paul Krugman (y los escépticos del colapso europeo) tienen razón**, pero están mirando variables diferentes.

*   **Garicano tiene razón (Paneles 1, 2 y 3 / Líneas Azul y Roja):** El declive tecnológico europeo es un hecho incontestable. Si medimos el tamaño de la economía en dólares corrientes a tipos de cambio de mercado, la brecha de competitividad y la fuga de talento (atraída por la explosión salarial en el sector transable estadounidense) son reales. Si Europa quiere liderar la inteligencia artificial o dominar industrias de frontera, está perdiendo la carrera estrepitosamente. 

*   **Krugman tiene razón (Panel 4 / Línea Verde):** El "Mito del Declive" tiende a exagerarse cuando omitimos el bienestar y el nivel de vida real de los ciudadanos. La aparente inferioridad europea es mucho más estrecha cuando deflactamos el consumo usando la Paridad de Poder Adquisitivo (PPA) y penalizamos la fatiga laboral (CEV). Gracias a un sector de servicios sociales eficiente, el ciudadano europeo mantiene un estándar de bienestar tremendamente competitivo, mientras que el espectacular salario del país dinámico se evapora al intentar pagar servicios locales ineficientes y carísimos.

En resumen: **Europa ha perdido claramente la carrera de la producción tecnológica global en términos de crecimiento nominal, pero mantiene una brecha de bienestar muchísimo más estrecha gracias a su estructura de precios y protección social**. Ambos enfoques son matemáticamente compatibles dentro de un mismo modelo económico neoclásico cerrado de forma limpia y honesta.
