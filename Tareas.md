# Tareas

En este apartado voy a listar las tareas para tener un seguimiento de lo que se hizo y lo que falta hacer.

**SMCDAModel**

* [X] Crear el método `__init__()` para crear la instancia.
* [X] Crear el método para declarar el `alias`.
* [X] Crear el método para declarar el `output_dir`.
* [X] Crear el método para declarar el `crs`.
* [X] Crear el método para añadir un `criterio`.
* [ ] Crear el método para añadir una `capa` a un `criterio`.
* [ ] Crear el método para añadir una `capa` a la `region_factible`.
* [ ] Crear el método para derivar los `ponderadores`.
* [ ] Crear método para explicar los conceptos del modelo.
* [-] Crear el método `__print__()`. FALTA chequear la importancia (es necesario SMCDACriteria).

**SMCDACriteria**

* [X] Crear el método `__init__()` para crear la instancia.
* [X] Crear el método para declarar el `alias`.
* [X] Crear el método para declarar el `importancia`.
* [X] Crear el método para añadir una `capa` al `criterio`.
* [ ] Crear el método para derivar los `ponderadores`.
* [-] Crear el método `__print__()` para verlo en la consola de forma prolija.

**SMCDALayer**

* [X] Crear método `__init__()` para crear la instancia.
* [X] Crear método para declarar el `alias`.
* [X] Crear método para declarar el `path` (directorio + nombre del archivo).
* [X] Crear método para declarar si la capa entra con signo `positivo` (si es deseable o indeseable).
* [X] Crear método para declarar el `elemento_neutral`.
* [X] Crear método para obtener la lista de `campos` (solo para capas vectoriales).
* [X] Crear método para declarar el `campo` a utilizar.
* [X] Crear método para declarar un `buffer` (solo para capas vectoriales).
* [X] Crear método para declarar un `proximity` (solo para capas vectoriales).
* [ ] Crear método para explicar los conceptos de la capa.
* [ ] Crear método `__print__()` para verlo en la consola de forma prolija.

**Funciones**

* [ ] Crear función para `reproyectar` la capa.
* [ ] Crear función para computar un `buffer` (solo para capas vectoriales).
* [ ] Crear función para computar un `proximity`.
* [ ] Crear función para `normalizar` (solo para capas vectoriales).
* [ ] Crear función para `procesar` el modelo.

**Demo**

* [ ] Crear una carpeta con 2 capas. Una vectorial y otra de ráster.
* [ ] Crear un script que ejecute el análisis.