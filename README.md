# Análisis Espacial Multicriterio

## Introducción al problema

El objetivo del programa es obtener un indicador que represente qué tan "valiosa" es la locación para construir una escuela. Para ello se ha planteado realizar un análisis espacial teniendo en cuenta aspectos socioeconómicas y ambientales. La idea era mantener la implementación lo suficientemente flexible como para incorporar o quitar diferentes características (ya que estos factores no son los mismos para escuelas primarias y secundarias) y que sirva como un método para analizar no solo la contrucción de escuelas, sino también, evaluar, por ejemplo, dónde sería conveniente ampliar la jornada escolar. Es por ello que por, parte del equipo de trabajo, se planteó implementar el análisis espacial multicriterio; derivado del hallazgo del artículo de Buzai (2014).

## Estado actual 
El resultado del programa se puede ver, en el siguiente 
[link](https://abc.gob.ar/secretarias/sites/default/files/2023-07/INDICE%20DE%20PRIORIDAD%20DE%20AMPLIACION%20DE%20LA%20OFERTA%20EDUCATIVA%20DEL%20NIVEL%20INICIAL%20PRIMARIO%20Y%20SECUNDARIO.pdf), el reporte de la dirección general de educación. El código todavía no está terminado, ya que la primera versión no era muy user friendly. La idea es construir clases para mejorar la declaración de información para luego ejecutar el procedimiento, el cual no ha cambiado.

## Breve descripción del análisis multicriterio

Una característica predominante en este tipo de problemas es que se deben evaluar varias alternativas bajo diferentes características deseables &mdash;que llamaremos "criterios" u "objetivos"&mdash; y obtener la mejor entre ellas. En la literatura se conocen a estos problemas como problemas multiobjetivos, de la cual tomaré varios conceptos. 

El primer concepto de gran utilidad a tener en mente es el de alternativa "factible". Definido de forma informal &mdash;al igual que todas las definiciones que daré aquí&mdash; como aquellas alternativas que están al alcance de la organización. En el caso del indicador planteado, estas alternativas serán aquellas localicaciones en las que se pueda construir una escuela. Un ejemplo es el de no tener en cuenta la superficie del mar o de los ríos.

Otro concepto es el de alternativa "ideal". Una alternativa es ideal si es mejor al resto de las alternativas en todas las características que se buscan que cumpla. En el caos de que esta alternativa exista, no sería necesario realizar este análisis, la respuesta es fácil, elegir la alternativa ideal. Sin embargo, es usual que esta alternativa no exista o no sea factible. Es por ello que debemos analizar las alternativas bajo otro criterio.

Este segundo criterio es el que se conoce como alternativa "eficiente". Este concepto engloba a aquellas alternativas que son mejores en algunos criterios, pero no en todos. Permite descartar una gran cantidad de alternativas, sin embargo, no nos brinda cuál es "mejor" entre dos soluciones eficientes.

Antes de continuar, voy a comentar algo sobre los problemas multiobjetivos. Existen muchos métodos para encontrar alternativas eficientes de un problema, dependiendo de este, algunos serán mejores que otros. En la literatura de análisis multicriterio, se utiliza, en casi la totalidad de los casos, el método "minisum". Este método consiste en asignar unos pesos arbitrarios a las diferentes funciones objetivos (estas funciones asignas un valor a cada alternativa analizada, para cada criterio) y se resuelve el problema. Por varios teoremas se sabe que la solución del problema "minisum" es una alternativa "eficiente". Su gran uso en el análisis multicriterio radica en el uso de pesos, ya que brinda una forma concreta de medir los distintos criterios bajo una misma medida.

Es en este punto que se debe dar un orden de preferencia a los criterios y analizar las alternativas bajo esa preferencia. En la literatura es usual simplificar al responsable de esta tarea a áquel individuo, o grupo, que debe tomar la decisión. Obviamente que la "mejor" alternativa que se obtendrá es subjetiva a los pesos dados por quien toma las decisiones. Si bien esto parece una desventaja, creo que es lo contrario, ya que permite establecer de forma clara cuales son esas preferencias y analizar las soluciones bajo diferentes tipos de preferencias para obtener su sensibilidad.

En el párrafo anterior se mencionó al pasar que se deben dar pesos a los diferentes criterios, como si fuese algo sencillo, pero, en muchos casos, esto puede no serlo. Primero, el concepto de pesos puede no ser tan amigable por razones cognitivas; segundo, no resulta fácil comparar dos criterios, mucho menos realizarla para más de dos criterios. Es por ello que en la literatura se han postulado diferentes técnicas para que la obtención de los pesos sea cognitivamente más sencilla. En esta implementación voy a utilizar en primer lugar, un ordenamiento de los criterios por su orden de importancia, se utilizará un criterio como base y se pedirá la importancia relativa entre los criterios y el criterio base. Dichos valores luego se traducirán en pesos para construir al función objetivo general/indicador.

## Aspecto Técnico de la implementación

### Workflow

El workflow que tengo pensado, para implementar el análisis, es el siguiente:

- Crear una instancia de la clase `SMCDAModel`, para representar al modelo y poder agregar información general.
- Asignar información general del modelo, como su `alias` (para identificar la especificaciones del resultado), el directorio de salida (`output_dir`, donde se va a guardar el resultado), los `criterios` y la región factible, entre otras cosas.
- Asignar las variables (que de ahora en más denominaré capas/layers por su representación espacial), declarar información para su manipulación y la forma de uso (si es una caracerística deseable o indeseable, si se debe emplear algún procesamiento, etcétera).
- Realizar el ordenamiento de las variables dentro de cada criterio, y hacer lo mismo para los distintos criterios.
- Ejecutar el análisis con toda la información. Es en este paso donde se realizan todos los procesos.

### Indicador, capas y pesos

El indicador se formará de la siguiente forma:

$$
    Rdo = \left(\prod_{j \in J}z_{j}\right)\left(\sum_{p \in P}\alpha_{p}\sum_{k=1 \in K_{p}}\omega_{k}x_{k}\right)
$$,

$J$ es el conjunto de capas que conforman la región factible y $z_{j}$ es la $j$-ésima capa; $P$ es el conjunto de criterios y $\alpha_{p}$ es el peso que obtuvo en base a las importancias asignadas; por último, $K_{p}$ es el conjunto de capas que conforman al criterio $p$, $\omega_{k}$ es el peso de la capa en el criterio y $x_{k}$ es la $k$-ésima capa.

Como se puede ver, se trata básicamente de realizar operaciones matriciales de suma y multiplicación. La fórmula permite entender cómo se comportarán las diferentes capas, y las características que deben tener las mismas. Por ejemplo, es recomendable que las capas de la región factible sean dicotómicas (tomen valores $0$ y $1$ solamente), para identificar apropiadamente las zonas factibles. Es posible agregar variables que no sean dicotómicas en la región factible, pero uno debe estar conciente de cómo impactará su incorporación de forma multiplicativas a TODAS las capas.

Por otro lado, todas las capas que conforman a los criterios entran de forma aditiva al indicador. El problema de esto es que es muy probable que no estén representados en las mismas unidades y sus escalas difieran, lo que afectaría el análisis, ya que aquellas capas con escalas de mayor magnitud estarían sobrerepresentadas. El programa lo resuelve tipificando a las capas para que su mínimo sea $0$ y su máximo $1$. 

Otro punto a destacar es que, como todas las capas entran sumando, tal vez no representen de forma adecuada la deseabilidad de la zona. Si tenemos una capa que muestra que tan "indeseable" es la zona, deberíamos transformarla para que tenga una escala para que represente que tan "deseable" es la zona. Por ejemplo, tenemos una capa que mide el riesgo hídrico, cuya escala puede ser 1:= riesgo bajo y 5:= riesgo alto. Si utilizamos esta capa sin modificaciones estaríamos pensando que mayor riesgo hídrico es más deseable, cuando, usualmente, sería lo contrario. Una de las posibilidades es modificar la capa para que refleje la deseabilidad como se desea. 

El programa puede manejar transformaciones básicas a través del parámetro `positive`. Este parámetro permite declararle al programa si una capa es "positiva", es decir, su escala representa que a mayor valor, mejor es la alternativa. Si se declara que la capa es "negativa", el programa la transformará de la siguiente manera: $\tilde{x}_{k} = (1 - x_{k})$. Con esta transformación la escala de la nueva capa ahora representa la deseabilidad de la zona. 

Otro punto relevante del manejo de las capas es cómo el programa maneja la diferencia de extensiones y los datos faltantes. Lo mas probable es que las extensiones geográficas de las diferentes capas no coincida, es por eso que el programa revisará las extensiones de todas las capas de la región factible, y utilizará la máxima extensión posible. Esto va a ampliar la extensión de todas las capas, pero en dichas zonas no tenemos datos, por lo que es necesario asignarle un valor. Lo mismo sucede para las zonas con datos faltantes dentro de la capa. Este valor se asigna a través del parámetro `na`. Lo usual es que dicho valor sea $0$, sin embargo pueden haber ocasiones en los que se requiera que se asigne el valor $1$. Esta imputación de datos se realiza antes de la transformación mencionada en el párrafo anterior, por lo tanto, si una capa es negativa, su transformación, $\tilde{x}_{k}$, tendrá asignado el valor $1$ en aquellas zonas donde $x_{k}$ tenía datos faltantes.

## Referencias

Buzai, G. D. (2014). Evaluación multicriterio y análisis espacial de los servicios de salud: conceptos centrales y aplicaciones realizadas a la ciudad de Luján.