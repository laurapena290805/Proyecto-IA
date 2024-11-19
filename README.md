# **Proyecto de Inteligencia Artificial**

**Integrantes:**
- *Laura Tatiana Coicue*
- *Laura Sofia Peñaloza*
- *Diego Alejandro Parra*
- *Santiago Reyes*


## Descripcion del proyecto 
En el proyecto se busca la implementación de los algoritmos vistos en clase, esto con el fin de solucionar el problema del ráton que busca llegar al queso. Para el desarrollo de este proyecto, se tuvo en cuenta
que muy probablemente los laberintos de prueba sean muy grandes, y por ende, puede que al implementar un solo algoritmo puede muy seguramente caer en ciclo, lo que nos lleva a pensar que el alternar los algoritmos 
de froma aleatoria podria ofrecer una solucion mucha más eficaz y segura. Las búsquedas que se implementaron en este proyecto son:
- Búsqueda por Amplitud
- Búsqueda por Profundidad
- Búsqueda por Profundidad Limitada
- Búsqueda por Profundidad Iterativa
- Búsqueda por Costo Uniforme
- Búsqueda Avara

## EJECUCION DEL PROYECTO
Para ejecutar el proyecto se debe tener en cuenta que se debe tener instalado python en su computador, y tener instalado el modulo de numpy, para instalarlo se debe ejecutar el siguiente comando:

```bash
pip install numpy
```
Una vez instalado el modulo de numpy, se debe ejecutar el archivo api.py, para esto se debe ejecutar el siguiente comando:

```bash
python api.py
```
Una vez ejecutado el comando, debe ir a la carpeta *Release* y ejecutar el ejecutable *agent_mouse.exe*. Está en este directorio:

```bash
Release/agent_mouse.exe
```
Una vez ejecutado el ejecutable, se le mostrará una ventana en la cual podrá seleccionar el algoritmo que desea utilizar para la busqueda del queso, y una vez seleccionado el algoritmo, se le mostrará el laberinto con la solución encontrada por el algoritmo seleccionado.

## Importante
Si llega a presentar algun problema con la ejecución del proyecto, solo debe volver a ejecutar el archivo *api.py* y volver a ejecutar el ejecutable *agent_mouse.exe*.
