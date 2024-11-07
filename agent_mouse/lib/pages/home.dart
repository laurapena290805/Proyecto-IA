import 'dart:io';

import 'package:agent_mouse/utils/styles.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:agent_mouse/utils/buttonGrid.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Icon(Icons.mouse_outlined),
        centerTitle: true,
        //delineado del appbar
        shape: const RoundedRectangleBorder(
          side: BorderSide(
            color: Color.fromARGB(41, 0, 0, 0),
          ),
        ),
      ),
      body: const SingleChildScrollView(
        child: Column(
          children: [
            HeaderWidget(),
            CentralContainer(),
            ListItemsWidget(),
            FooterWidget(),
          ],
        ),
      ),
    );
  }
}

class HeaderWidget extends StatelessWidget {
  const HeaderWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      // Espaciado interno
      padding: const EdgeInsets.all(40),
      width: MediaQuery.of(context).size.width,
      color: const Color.fromARGB(255, 255, 255, 255),
      //Titulo, subtitulo y botón
      child: Column(
        children: [
          const Text(
            'Agent Mouse',
            style: AppStyles.titleTextStyle,
          ),
          //const SizedBox(height: 10),
          const Text(
            'Buscando el queso',
            style: AppStyles.subtitleTextStyle,
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: () {
              // Acción al tocar el botón
            },
            child: const Text('Botón', style: AppStyles.buttonTextStyle),
          ),
          const SizedBox(height: 20),
        ],
      ),
    );
  }
}

class CentralContainer extends StatefulWidget {
  const CentralContainer({super.key});

  @override
  // ignore: library_private_types_in_public_api
  _CentralContainerState createState() => _CentralContainerState();
}

class _CentralContainerState extends State<CentralContainer> {
  // Marcador seleccionado: 1 para azul/círculo, 2 para verde/check, 3 para rojo/X
  int selectedMarker = 1;
  String algoritmoSeleccionado = 'limitada_profundidad';

  bool isLoading = false;

  ButtonGrid myButtonGrid =
      const ButtonGrid(rows: 5, columns: 5, selectedMarker: 1);

  // Función para cambiar el marcador
  void setMarker(int marker) {
    setState(() {
      selectedMarker = marker;
    });
  }

  @override
  Widget build(BuildContext context) {
    //Contenedor que estará divido 2: para dentro de cada uno tenga
    return Container(
      //Separacion en las esquinas horizontales
      padding: const EdgeInsets.symmetric(horizontal: 50),
      color: const Color.fromARGB(255, 255, 255, 255),

      child: Column(
        children: [
          const SizedBox(height: 20),
          Row(
            children: [
              Expanded(
                child: Container(
                    //Es un cuadrado redondeado que se ajusta al tamaño de la pantalla

                    width: MediaQuery.of(context).size.width *
                        0.8, // Ancho 80% del ancho de la pantalla
                    height: MediaQuery.of(context).size.height *
                        0.6, // Alto 60% del alto de la pantalla
                    //muestra una imagen en C:\Users\santi\OneDrive\Documentos\Proyecto-IA\arbol.png

                    decoration: const BoxDecoration(
                        borderRadius: BorderRadius.all(Radius.circular(20)),
                        color: Color.fromARGB(75, 179, 179, 179)),
                    child: Padding(
                      padding: const EdgeInsets.all(20),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(20),
                        child: Image.asset(
                          'lib/assets/arbol.png',
                          fit: BoxFit.cover,
                        ),
                      ),
                    )),
              ),
              const SizedBox(width: 20),
              Expanded(
                  child: Container(
                width: MediaQuery.of(context).size.width *
                    0.8, // Ancho 80% del ancho de la pantalla
                height: MediaQuery.of(context).size.height *
                    0.6, // Alto 60% del alto de la pantalla
                decoration: const BoxDecoration(
                    color: Color.fromARGB(75, 179, 179, 179)),
                child: ButtonGrid(
                  rows: 4,
                  columns: 4,
                  selectedMarker: selectedMarker,
                ),
              ) // Llama a ButtonGrid aquí
                  ),
            ],
          ),
          const SizedBox(height: 20),
          Container(
              padding: const EdgeInsets.all(40),
              width: MediaQuery.of(context).size.width,
              color: const Color.fromARGB(255, 255, 255, 255),
              //El contenedor tendra 2 botones simetricos, uno desde la izquierda al centro y el otro del centro a la derecha, dejando un espacio en el centro
              //los botones seran semicuadrados
              child: Column(children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ElevatedButton(
                      onPressed: () => setMarker(1),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: selectedMarker == 1
                            ? Colors.blue // Azul completo
                            : const Color.fromARGB(
                                131, 96, 125, 139), // Gris desaturado
                      ),
                      child: const Icon(Icons.circle, color: Colors.white),
                    ),
                    ElevatedButton(
                      onPressed: () => setMarker(2),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: selectedMarker == 2
                            ? Colors.green // Verde completo
                            : Colors.green[100], // Gris verdoso
                      ),
                      child: const Icon(Icons.check, color: Colors.white),
                    ),
                    ElevatedButton(
                      //Boton con un icono de X y una descripción
                      onPressed: () => setMarker(3),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: selectedMarker == 3
                            ? Colors.red // Rojo completo
                            : Colors.red[100], // Gris rojizo
                      ),
                      child: const Icon(Icons.close, color: Colors.white),
                    ),
                  ],
                ),
                const SizedBox(height: 5),
                const Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    Text(
                      '    Salida        ',
                      style: AppStyles.infomationTextStyle,
                    ),
                    Text(
                      'Meta      ',
                      style: AppStyles.infomationTextStyle,
                    ),
                    Text(
                      'Bloqueos  ',
                      style: AppStyles.infomationTextStyle,
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                //Boton para iniciar
                ElevatedButton(
                  onPressed: () {
                    // Acción al tocar el botón
                    _runAlgorithm();
                  },
                  child:
                      const Text('Iniciar', style: AppStyles.buttonTextStyle),
                ),
              ])),
          const SizedBox(height: 20),
        ],
      ),
    );
  }

  Process? _pythonProcess; // Variable para almacenar el proceso del servidor

  @override
  void initState() {
    super.initState();
    _startPythonServer();
  }

  Future<void> _startPythonServer() async {
    try {
      //Buscar la ruta del archivo para que funcione en cualquier dispositivo(Windows, Linux, Mac) que esta en /Proyecto-IA/API.py
      const pythonScriptPath =
          'C:/Users/santi/OneDrive/Documentos/Proyecto-IA/API.py'; // Ruta del script de Python

      _pythonProcess = await Process.start('python', [pythonScriptPath]);
      print('Servidor Python iniciado');

      // Escuchar la salida del proceso para depurar
      _pythonProcess!.stdout.transform(utf8.decoder).listen((data) {
        print(data);
      });
    } catch (e) {
      print('Error al iniciar el servidor: $e;;');
    }
  }

  @override
  void dispose() {
    if (kDebugMode) {
      print('dispose() llamado');
    } // Para verificar si se llama
    _stopPythonServer();
    super.dispose();
  }

  Future<void> _stopPythonServer() async {
    if (_pythonProcess != null) {
      // Intenta cerrar el proceso
      _pythonProcess!.kill();

      // Espera un poco para asegurarte de que el proceso se cierre
      await Future.delayed(
          const Duration(seconds: 1)); // Ajusta el tiempo si es necesario

      // Verifica si el proceso sigue corriendo
      print('Servidor cerrado.');
    }
  }

  // Función para ejecutar el algoritmo en el servidor
  Future<void> _runAlgorithm() async {
    setState(() {
      isLoading = true;
      //resultado = ''; // Reiniciar resultado
    });

    try {
      print('Ejecutando algoritmo...');
      print(myButtonGrid.displayMatrix);
      print(myButtonGrid.blueButtonIndex);
      print(myButtonGrid.greenButtonIndex);

      final response = await http.post(
        Uri.parse('http://127.0.0.1:5000/algorithms'),
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: json.encode({
          /*
          'A': int.parse(aController.text),
          'B': int.parse(bController.text),
          'n': int.parse(nController.text),
          'ofertas': json
              .decode(ofertasController.text), // Ofertas en formato correcto
          'algoritmo': algoritmoSeleccionado // Algoritmo seleccionado
          */
          'Inicio': myButtonGrid.blueButtonIndex, // Inicio
          'Meta': myButtonGrid.greenButtonIndex, // Meta
          'Mapa': myButtonGrid.displayMatrix, // Bloqueos
          'Algoritmo': algoritmoSeleccionado // Algoritmo seleccionado
        }),
      );
      print(response.statusCode);
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          print("Si se pudo ${data['confirmacion']} ");
          //resultado =
          //    'La mejor asignación es: ${data['resultado']}\nValor Final: ${data['asignacion']}';
        });
      } else {
        setState(() {
          //resultado = 'Error en la ejecución';
        });
      }
    } catch (e) {
      setState(() {
        //resultado = 'Error: $e';
      });
    } finally {
      setState(() {
        //isLoading = false; // Termina la carga
      });
    }
  }
}

void loaderImage() {
  // Cargar la imagen
}

class ListItemsWidget extends StatelessWidget {
  const ListItemsWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      shrinkWrap: true,
      physics:
          const NeverScrollableScrollPhysics(), // Para permitir el desplazamiento del SingleChildScrollView
      itemCount: 20, // Número de elementos en la lista
      itemBuilder: (context, index) {
        return ListTile(
          title: Text('Elemento $index'),
          onTap: () {
            // Acción al tocar el elemento
          },
        );
      },
    );
  }
}

class FooterWidget extends StatelessWidget {
  const FooterWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      color: Colors.grey,
      child: const Text(
        'Pie de página',
        style: AppStyles.infomationTextStyle,
      ),
    );
  }
}
