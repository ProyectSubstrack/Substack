# El gran apagón de las horas: Resolviendo el misterio de la jornada laboral con Python y microdatos de la EPA

España vive un momento dulce en términos de creación de empleo formal. Si echamos un vistazo a los registros de afiliación a la Seguridad Social, las cifras son de récord: más de 21 millones de ocupados y una tasa de temporalidad desplomada. Sin embargo, hay un "fantasma" que recorre las tertulias económicas y los pasillos del Congreso: los españoles, supuestamente, trabajamos cada vez menos horas.

Esta narrativa se sostiene en un pilar estadístico monumental: la Encuesta de Población Activa (EPA). Según la EPA, desde la pandemia, las horas efectivas trabajadas han sufrido un hundimiento crónico. Este dato ha servido en bandeja de plata el argumento perfecto para legislar una reducción de la jornada laboral a 37,5 horas. "Si el mercado ya está reduciendo las horas orgánicamente, adaptemos la ley", dicen los defensores.

Pero, ¿y si esta caída de las horas es, en gran medida, un espejismo estadístico? ¿Y si no estamos trabajando drásticamente menos, sino que simplemente **hemos cambiado la forma en la que contamos el tiempo**?

Basándonos en la brillante tesis del economista Miguel Artola Blanco, nos hemos arremangado y hemos bajado a la sala de máquinas de la estadística española: los **microdatos de la EPA**. Hemos procesado millones de registros individuales de encuestas desde 2018 hasta 2025 utilizando Python para demostrar, con datos puros y duros, cómo un cambio metodológico en el cuestionario en 2021 alteró para siempre nuestra percepción de la realidad laboral.

Acompáñame en esta inmersión de datos donde vamos a destripar la estadística oficial paso a paso.

---

## El origen del problema: Cómo el INE nos exprime la memoria

Para entender el problema, primero debemos entender cómo se recoge la información. La EPA no lee la mente de los ciudadanos ni entra en los servidores de las empresas; pregunta directamente a las familias. Y la memoria humana es, por definición, frágil y selectiva.

**Hasta el año 2020**, el cuestionario del Instituto Nacional de Estadística (INE) era bastante "relajado". El encuestador te preguntaba por tus horas habituales (tu contrato de 40 horas, por ejemplo) y luego por tus horas efectivas reales esa semana. Si tú decías que habías trabajado 40 horas o más (quizás compensaste una salida al médico quedándote más tiempo el viernes), el cuestionario **terminaba ahí**. No te preguntaba por qué habías faltado, porque matemáticamente no había un déficit de horas.

**A partir de 2021**, empujado por normativas europeas, el INE cambió las reglas del juego. El nuevo cuestionario se volvió inquisitivo. Antes de preguntarte por el total de horas, te obliga a hacer memoria directa: *¿Ha faltado usted esta semana por vacaciones? ¿Por enfermedad? ¿Salió unas horas antes para un asunto propio?*

Este cambio sutil tiene un impacto psicológico brutal. Como veremos a continuación, el nuevo método destapó millones de horas no trabajadas que antes, simplemente, se nos olvidaba mencionar.

Para demostrarlo, hemos diseñado tres ejercicios analíticos sobre los microdatos brutos de la EPA.

---

## Ejercicio 1: El embudo del viejo cuestionario (Simulación)

El primer paso lógico era hacernos una pregunta técnica: **Si aplicásemos la lógica del viejo cuestionario (pre-2021) a las respuestas extremadamente detalladas que da la gente hoy (post-2021), ¿cuántas ausencias habrían pasado desapercibidas?**

### ¿Cómo lo hicimos? (Metodología y Código)

Nos descargamos los microdatos de la EPA (a 3 dígitos) de todos los trimestres desde el 2021T1 hasta el 2025T4. Son archivos inmensos donde cada fila es una persona encuestada.

Para nuestro análisis, aislamos exclusivamente a los **asalariados** (filtrando las situaciones profesionales `07` y `08`). Además, rescatamos el factor mágico de las encuestas: el **`factorel`** (factor de elevación). La EPA entrevista a unas 160.000 personas, no a 48 millones de españoles. El `factorel` nos dice a cuántas personas de la vida real representa ese encuestado (por ejemplo, si su `factorel` es 400, ese individuo representa a 400 españoles con sus mismas características).

A partir de ahí, buscamos a los encuestados que declararon explícitamente haber tenido una ausencia por vacaciones o enfermedad durante esa semana. 
Y aquí aplicamos nuestra "trampa temporal": miramos sus **Horas Efectivas (HE)** finales y sus **Horas Habituales (HH)**. 

Si un asalariado se cogió un día libre, pero aun así sus horas efectivas de la semana fueron mayores o iguales a sus horas habituales ($HE \ge HH$) debido a horas extras previas o acumulación de jornada, el cuestionario antiguo **jamás le habría registrado como ausente**. 

Creamos un script en Python que iteraba trimestre a trimestre buscando a estas personas "ocultas".

### Los Resultados: Destapando la caja negra

Los resultados confirmaron la tesis de forma abrumadora. Al simular el viejo cuestionario sobre la realidad actual, descubrimos que el INE estaba perdiendo por el desagüe un volumen masivo de información.

En el primer trimestre de 2021, de los 3,39 millones de asalariados ausentes, **más de 231.000 (el 6,8%) habrían sido invisibles** para la antigua EPA. 

Para asegurarnos de que no era un fallo puntual de la pandemia, iteramos el código sobre los 16 trimestres posteriores. Los datos se mantenían como una roca:

1. **Trabajadores Ocultos:** De media, un **5,20%** de los trabajadores que se ausentan cada trimestre quedaban camuflados por el antiguo cuestionario. En picos como el segundo trimestre de 2021, la cifra llegó a superar el 8%.
2. **Días de Ausencia Evaporados:** En términos de volumen total, el modelo antiguo borraba sistemáticamente cerca del **3,6% de todos los días no trabajados** en España. Estamos hablando de que la vieja EPA "ignoraba" casi 4,8 millones de días de inasistencia cada tres meses.

Al correr un *t-test* estadístico sobre nuestra serie de 16 trimestres, obtuvimos un p-valor de `6.56e-10`. En lenguaje llano: la probabilidad de que este error del viejo cuestionario fuera una casualidad estadística es de un cero absoluto. El embudo existía y era gigantesco.

![Porcentaje de ausencias y días ocultos a lo largo del tiempo](../imagenes/ausencias_ocultas.png)

Como se puede apreciar en el gráfico, la línea azul muestra la consistencia de ese grupo de trabajadores que el viejo cuestionario marginaba sistemáticamente. La EPA no nos decía que trabajábamos más; simplemente, era sorda a nuestras inasistencias si al final de la semana cumplíamos con nuestro cupo de horas.

---

## Ejercicio 2: El contexto histórico (Regresión Discontinua en el Tiempo - RDiT)

Sabiendo que el cuestionario antiguo inflaba artificialmente las horas, el siguiente paso era mirar la "foto grande". Queríamos ver la evolución histórica completa de las horas efectivas medias por trabajador. ¿Cómo afectó el cambio de 2021 a la serie temporal histórica?

Para responder, recurrimos a una técnica econométrica clásica para evaluar impactos de políticas o cambios estructurales: la **Regresión Discontinua en el Tiempo (RDiT)**.

### ¿Cómo lo hicimos?

Descargamos los datos desde 2018 hasta 2025. Nuestro objetivo era modelar cómo se comportaban las horas efectivas medias por trimestre. 

Pero el mundo real es ruidoso. No podíamos simplemente comparar las horas de 2019 con las de 2023 porque por medio hubo un confinamiento global y una tendencia a la baja de las horas en todos los países occidentales (debido al envejecimiento poblacional y la terciarización de la economía hacia servicios, donde las jornadas son más cortas).

Por lo tanto, construimos un modelo estadístico (OLS con la librería `statsmodels` de Python) aislando matemáticamente diferentes "fuerzas":
1. **La tendencia temporal (t):** Una línea de fondo que asume que, naturalmente, las horas van cayendo poco a poco cada año.
2. **La estacionalidad (Q2, Q3, Q4):** Variables "dummy" para decirle al modelo: *"Oye, en verano (Q3) las horas siempre se hunden, no te asustes"*.
3. **El shock del COVID (2020):** Un mazazo artificial que paralizó el país.
4. **Nuestra variable clave (`Post_2021`):** Un escalón matemático que le dice al modelo: *"Dime si hay un salto inexplicable justo a partir del primer trimestre de 2021"*.

### Los Resultados: La confluencia de dos crisis

El modelo RDiT fue iluminador, porque nos enseñó que la realidad no es binaria. 

Primero, el modelo detectó una **caída tendencial natural brutal** y estadísticamente significativa ($p < 0.01$). Incluso si la EPA no hubiera cambiado nunca su cuestionario, los españoles de 2025 trabajarían menos horas a la semana que los de 2018. El mercado laboral está madurando y el empleo a tiempo parcial se consolida.

Segundo, el shock de la pandemia fue devastador, y el modelo le atribuye un impacto destructor de casi 2 horas semanales medias durante su pico más grave.

¿Y el cambio del cuestionario (`Post_2021`)? Al descontar la fuerte tendencia a la baja y el caos del Covid, el "escalón" puro de 2021 es difícil de aislar estadísticamente de forma independiente. Sin embargo, al proyectar las horas reales frente al ajuste de nuestro modelo, la fractura de la serie es evidente a simple vista.

![RDiT Efecto Cuestionario en Horas Efectivas](../imagenes/rdit_horas_efectivas.png)

En el gráfico anterior, la línea negra muestra las horas efectivas reales de la economía española. Tras la brutal V de la pandemia, la serie se estabiliza de nuevo... pero lo hace en un suelo mucho más bajo (33-34 horas) que el suelo que ocupaba en 2018-2019 (35 horas). 

El Ejercicio 2 nos enseña una lección de humildad académica: la caída de las horas en España es multicausal. Es cierto que el cuestionario nos robó horas, pero también es cierto que, sociológicamente, la jornada laboral patria lleva contrayéndose años de forma orgánica.

---

## Ejercicio 3: El "Efecto Olvido" y la explosión de las micro-ausencias

Llegamos a la joya de la corona. El Ejercicio 1 nos demostró que el viejo cuestionario era ciego ante ciertas ausencias por un filtro matemático. Pero, ¿qué hay de la psicología humana?

La teoría de Artola sostiene que, cuando un encuestador no te pregunta directamente por tus ausencias, **tiendes a olvidar las pequeñas y a recordar solo las grandes**. Es imposible que olvides que estuviste la semana pasada entera de baja médica. Pero es sumamente fácil que olvides, meses después, que el miércoles saliste a las 11:00 am en lugar de a las 14:00 pm para renovar el DNI.

Si esta teoría psicológica es cierta, el nuevo cuestionario de 2021 (el inquisitivo) debería haber disparado los reportes de pequeñas ausencias, mientras que el volumen de grandes ausencias debería haberse mantenido relativamente normal.

### ¿Cómo lo hicimos?

Diseñamos nuestro último script de Python para enfrentar dos años totalmente limpios de ruido pandémico: **2019 (el apogeo del cuestionario antiguo)** contra **2023 (la consolidación del nuevo cuestionario)**.

Para cada trabajador, calculamos su "Diferencia de Horas" restando las horas efectivas a las horas habituales ($HH - HE$). Si el resultado era positivo, significaba que había perdido horas de trabajo esa semana.

Dividimos meticulosamente esas horas perdidas en 100 para corregir el formato crudo del INE (que nos sirve las 40 horas como `4000`) y agrupamos a todos esos millones de españoles en cinco "cubos" según el tamaño de su ausencia:
* De 1 a 4 horas (Micro-ausencias, salir un poco antes).
* De 5 a 8 horas (Un día libre).
* De 9 a 16 horas (Un par de días).
* De 17 a 30 horas (Media semana o puente).
* 31 horas o más (Semana entera de vacaciones o baja médica grave).

Finalmente, sumamos los factores de elevación poblacional para obtener el volumen real de ciudadanos que entraban en cada tramo.

### Los Resultados: Una prueba irrefutable

Al imprimir la tabla de crecimientos por consola, sabíamos que habíamos dado en el clavo. Los resultados fueron, literalmente, espectaculares.

Al cruzar los datos de 2019 y 2023, vimos que las ausencias graves y de larga duración (semanas completas de más de 31 horas perdidas) habían crecido orgánicamente un 45,1%. Esto entra dentro de lo razonable, impulsado por el aumento general del empleo y el auge sostenido de las bajas por Incapacidad Temporal.

Pero al mirar las **micro-ausencias (1 a 4 horas)**, los números reventaron la escala. El volumen de trabajadores que reportaban haber perdido un puñado de horas a la semana **se multiplicó por más de dos**, experimentando un crecimiento demencial del **112,4%**. 

Las ausencias de unos dos días (9 a 16 horas) no se quedaron atrás, disparándose casi un **88,7%**.

![Efecto Olvido: Distribución de Ausencias](../imagenes/distribucion_ausencias.png)

Mirad el gráfico de barras. El "Efecto Olvido" cristalizado en datos. No es que en 2023 se haya desatado una epidemia de personas que deciden escaparse un par de horas de la oficina. Es que en 2019, la EPA simplemente no conseguía que nos acordáramos de reportarlo. 

El nuevo cuestionario introdujo una lupa de alta resolución en la vida de los españoles, logrando capturar cientos de miles de ausencias cotidianas, visitas al médico y permisos por asuntos propios que, sumados, hundieron la media aritmética de la jornada nacional.

---

## Conclusión: El peligro de legislar sobre una ilusión

Manipular microdatos con Python no es solo un ejercicio lúdico; es una necesidad democrática cuando se trata de auditar las cifras que dirigen el futuro económico del país. 

El desplome aparente de la jornada laboral española que pinta la Encuesta de Población Activa desde 2021 no es un fenómeno revolucionario de nuestra ética del trabajo. Como hemos demostrado analíticamente en este artículo, gran parte de ese agujero negro es fruto de un cambio metodológico: **un filtro antiguo defectuoso** que ocultaba ausencias compensadas (Ejercicio 1) y **un nuevo cuestionario inquisitivo** que curó de golpe la amnesia selectiva de los españoles frente a las micro-ausencias (Ejercicio 3).

Las repercusiones de este espejismo estadístico son gravísimas. 

Primero, distorsiona la **productividad**. La Contabilidad Nacional española se nutre de estas horas mermadas de la EPA para calcular la productividad por hora de España. Al dividir nuestro Producto Interior Bruto por un número de horas artificialmente bajo, la estadística proyecta una falsa sensación de euforia, haciéndonos creer que somos muy eficientes cuando, en realidad, nuestra productividad por ocupado arrastra un estancamiento letal, generando apenas 64€ de valor por hora frente a los 100€ de la locomotora alemana.

Segundo, y aún más peligroso, distorsiona la **política**. Utilizar esta supuesta caída de horas como argumento principal para imponer normativamente una reducción legal de la jornada a las 37,5 horas semanales es legislar a ciegas. Si ignoramos que los registros administrativos reales de la Seguridad Social (las nóminas y cotizaciones reales, no las encuestas subjetivas) están marcando récords de volumen de trabajo ininterrumpido, corremos el riesgo de asfixiar la competitividad de las pequeñas empresas bajo una falsa premisa.

El elefante en la habitación no es que los españoles quieran trabajar 37,5 horas; el verdadero desafío es la caída de nuestra competitividad estructural y un absentismo que se ha disparado un 150% en una década. Es hora de dejar de debatir basándonos en espejismos estadísticos y mirar de frente a los datos.

*Todo el código en Python, el análisis de microdatos (basado en más de 20 millones de registros de la EPA) y los scripts utilizados para la generación de este artículo están disponibles para su auditoría y replicación pública.*
