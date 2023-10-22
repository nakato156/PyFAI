# Tabala de contenido

1. [**Descripción del problema**](#_descripcion)
    - [Detección de obstáculos](#_detecObs)
    - [Planificación de movimiento](#_planifMov)
    - [Evaluación del éxito](#_evaExito)
    - [Interfaz de usuario](#_interfaz)

2. [**Descripción del conjunto de datos**](#_descDataSet)  
3. [**Propuesta**](#_propuesta)  
4. [**Técnicas y metodología**](#_tecMetod)  
    - [Mecánica del juego](#_mecanica)  
    - [Objetivos y reglas](#_objReglas)  
    - [Optimización y rendimiento](#_optmiz)

5. [**Bibliografía**](#_biblio)

# <a name="_descripcion"></a>**Descripción del problema**

El objetivo principal de este proyecto es diseñar un bot capaz de jugar de manera autónoma el juego Frogger. Frogger es un juego clásico de arcade en el que un jugador controla a una rana que debe cruzar una carretera llena de obstáculos y un río con troncos y tortugas en movimiento. El desafío radica en evitar ser golpeado por vehículos en la carretera y caer al agua en el río.

El bot debe abordar los siguientes desafíos clave:

## <a name="_detecObs"></a>**Detección de obstáculos** 
Como en la vida cotidiana hay muchas cosas que utilizan la detección de objetos, por ejemplo los coches autónomos. Según (colaboradores de Wikipedia, 2023) La detección de objetos es una tecnología de ordenador relacionada con la visión artificial y el procesamiento de imagen que trata de detectar casos de objetos semánticos de una cierta clase. Para nuestro caso no usaremos una detección de objetos basada en visión artificial. El bot desarrollado debe ser capaz de identificar y rastrear la posición de vehículos, troncos y tortugas en movimiento en tiempo real para evitar colisiones y asegurarse de que la rana llegue a salvo al otro lado de la pantalla. Según los parámetros que recibe del entorno.

## <a name="_planifMov"></a>**Planificación de movimiento** 
El bot debe tomar decisiones inteligentes sobre cuándo y cómo moverse, considerando factores como la velocidad de los obstáculos,  la ubicación de la rana y los posibles lugares de destino en el río. Para esto usaremos el algoritmo Bellman-Ford (Wikipedia contributors, 2023). Transformaremos el juego en un grafo y encontraremos el camino más corto desde donde estamos hasta el final. Esto nos ayudará a planificar el movimiento de nuestra rana hacia la meta.

1. ## <a name="_evaExito"></a>**Evaluación del éxito** 
   El bot debe estar programado para reconocer cuándo ha tenido éxito en cruzar con éxito a la rana al otro lado de la pantalla y, por lo tanto, ganar puntos en el juego. Es decir, guardar los intentos con sus resultados.

2. ## <a name="_interfaz"></a>**Interfaz de usuario:** 
   Se debe proporcionar una interfaz de usuario que permita a los usuarios observar y controlar el progreso del bot y, posiblemente, ajustar su nivel de dificultad. 

   Este proyecto implica un desafío técnico significativo en términos de visión por computadora, toma de decisiones algorítmicas y diseño de interfaz. 


# <a name="_descDataSet"></a>**Descripción del conjunto de datos** 
Nuestro conjunto de datos se basa en todo el tablero. El tablero del juego se convierte en un grafo ponderado dirigido en el cual nuestra rana tendrá que ir de un nodo inicial (I) hasta un nodo final (F).
Un tamaño aproximado de nuestro tablero será de 30 x 50. Haciendo que, en el mejor de los casos, existan 1500 nodos que recorrer. Pero nuestro bot, al momento de utilizar los algoritmos mencionados, recorrerá más de 1500 nodos para poder encontrar el camino correcto para poder llegar a la meta.
Además, consideramos el uso de dos algoritmos diferentes, por lo cual, el espacio de búsqueda se duplica. El tener dos algoritmos, aparte de aumentar nuestro espacio de búsqueda, nos permitirá saber y comparar, con qué algoritmo la rana llega primero.  


![](grafo-tablero.png)

# <a name="_propuesta"></a>**Propuesta**
Este proyecto tiene como objetivo desarrollar un bot autónomo para el juego Frogger, un juego de arcade clásico. Frogger desafía a los jugadores a guiar una rana a través de una carretera llena de obstáculos y un río con troncos y tortugas en movimiento. El bot se enfrentará a desafíos clave, incluyendo la detección de obstáculos, planificación de movimiento, evaluación de éxito y una interfaz de usuario.

# <a name="_tecMetod"></a>**Técnicas y metodología:**
## <a name="_mecanica"></a>**Mecánica del juego** 
- Mantendremos la mecánica del juego original. El juego, los personajes, obstáculos y más serán como se conoce.
## <a name="_objReglas"></a>**Objetivos y reglas**
- Los objetivos son los originales, avanzar lo más que se pueda, evitando obstáculos, evitar caer al agua, ser atropellado, etc.
- Se tendrá 3 vidas cada vez que se inicia el juego, si chocas contra un obstáculo el juego se reiniciará y perderás una vida.

## <a name="_optmiz"></a>**Optimización y rendimiento**
- Usaremos la técnica de memoización para optimizar el juego y el bot, para que su proceso sea más rápido. 

<a name="_ct2wc56m8klz"></a>
# <a name="_biblio"></a>**Bibliografía** 
- Printista, A. M. (2000, 1 octubre). *Una implementación paralela del algoritmo de Q-Learning basada en un esquema de comunicación con caché*. <http://sedici.unlp.edu.ar/handle/10915/23363> 

- Colaboradores de Wikipedia. (2023). Detección de objetos. *Wikipedia, la enciclopedia libre*. <https://es.wikipedia.org/wiki/Detecci%C3%B3n_de_objetos>

- Wikipedia contributors. (2023). Bellman–Ford Algorithm. *Wikipedia*. <https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm> 



