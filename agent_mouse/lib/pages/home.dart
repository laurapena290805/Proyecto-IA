import 'package:agent_mouse/utils/styles.dart';
import 'package:flutter/material.dart';
import 'package:agent_mouse/utils/buttonGrid.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';
import 'package:file_picker/file_picker.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Icon(Icons.mouse_outlined),
        centerTitle: true,
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
      padding: const EdgeInsets.all(40),
      width: MediaQuery.of(context).size.width,
      color: const Color.fromARGB(255, 255, 255, 255),
      child: const Column(
        children: [
          Text(
            'Agent Mouse',
            style: AppStyles.titleTextStyle,
          ),
          Text(
            'Buscando el queso',
            style: AppStyles.subtitleTextStyle,
          ),
          SizedBox(height: 20),
          Text(
            '¡Bienvenido a Agent Mouse! Ayuda al ratón a encontrar el queso en el laberinto. Ingresa los datos y configura el laberinto para comenzar la búsqueda.',
            style: AppStyles.infomationTextStyle,
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}

class CentralContainer extends StatefulWidget {
  const CentralContainer({super.key});

  @override
  _CentralContainerState createState() => _CentralContainerState();
}

class _CentralContainerState extends State<CentralContainer> {
  int selectedMarker = 1;
  String algoritmoSeleccionado = 'limitada_profundidad';
  late ButtonState buttonState;
  bool isLoading = false;
  bool isConfigured = false;
  bool isReadFile = false;
  int rows = 0;
  int columns = 0;
  final inicio = [0, 0];
  final meta = [0, 0];
  bool isInicioSet = false; // Nueva variable
  bool isMetaSet = false; // Nueva variable
  int iterations = 0;
  List<List<String>>? mapa;
  String? fileName;
  String algoritmoActual = '';

  final TextEditingController rowsController = TextEditingController();
  final TextEditingController columnsController = TextEditingController();
  final TextEditingController iterationsController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 50),
      color: const Color.fromARGB(255, 255, 255, 255),
      child: Column(
        children: [
////////////////////////////////////// CONTENIDO DE EJECUCION ////////////////////////////////////
          Text(
            isConfigured
                ? '¡Modifica tu laberinto e inicia!'
                : 'Configura a tu ratón ingresando los siguientes datos',
            style: const TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.bold,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 10),
          if (isConfigured)
            Column(
              children: [
                Row(
                  children: [
////////////////////////////////////// CONTENIDO DE LABERINTO ////////////////////////////////////
                    Expanded(
                      child: Center(
                        child: Container(
                          // Tamaño fijo para el contenedor cuadrado
                          width:
                              300, // Puedes ajustar este valor según tus necesidades
                          height:
                              300, // Asegúrate de que la altura sea igual al ancho para que sea un cuadrado
                          decoration: const BoxDecoration(
                            color: Color.fromARGB(255, 255, 255, 255),
                          ),
                          child: ButtonGrid(
                            rows: rows,
                            columns: columns,
                            selectedMarker: selectedMarker,
                            matrizCargada: mapa, // Pasar la matriz cargada
                            onUpdateInicio: (row, col) {
                              setState(() {
                                inicio[0] = row;
                                inicio[1] = col;
                                isInicioSet =
                                    true; // Actualizar la variable booleana
                              });
                            },
                            onUpdateMeta: (row, col) {
                              setState(() {
                                meta[0] = row;
                                meta[1] = col;
                                isMetaSet =
                                    true; // Actualizar la variable booleana
                              });
                            },
                            onUpdateMatriz: (matriz) {
                              setState(() {
                                mapa = matriz;
                              });
                            },
                          ),
                        ),
                      ),
                    ),
                  ],
                ),

////////////////////////////////////// CONTENIDO DE BOTONES ////////////////////////////////////
                Container(
                  padding: const EdgeInsets.all(40),
                  width: MediaQuery.of(context).size.width,
                  color: const Color.fromARGB(255, 255, 255, 255),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          ElevatedButton(
                            onPressed: () => setMarker(1),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: selectedMarker == 1
                                  ? Colors.blue
                                  : const Color.fromARGB(131, 96, 125, 139),
                            ),
                            child:
                                const Icon(Icons.circle, color: Colors.white),
                          ),
                          ElevatedButton(
                            onPressed: () => setMarker(2),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: selectedMarker == 2
                                  ? Colors.green
                                  : Colors.green[100],
                            ),
                            child: const Icon(Icons.check, color: Colors.white),
                          ),
                          ElevatedButton(
                            onPressed: () => setMarker(3),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: selectedMarker == 3
                                  ? Colors.red
                                  : Colors.red[100],
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
                      // Al dar click en el botón, se ejecuta el algoritmo y se bloquea el botón hasta que el algoritmo termine
                      ElevatedButton(
                        onPressed: isLoading ? null : _runAlgorithm,
                        child: isLoading
                            ? const CircularProgressIndicator()
                            : const Text('Iniciar búsqueda'),
                      ),
                    ],
                  ),
                ),
              ],
            ),

////////////////////////////////////// CONTENIDO DE CONFIGURACION ////////////////////////////////////

          const SizedBox(height: 20),
          Center(
            child: SizedBox(
              width: 300, // Ajusta este valor según tus necesidades
              child: Column(
                children: [
                  TextField(
                    controller: rowsController,
                    decoration: const InputDecoration(
                      labelText: 'Número de filas (n)',
                      border: OutlineInputBorder(),
                    ),
                    keyboardType: TextInputType.number,
                    enabled: mapa ==
                        null, // Bloquear entrada si hay una matriz cargada
                  ),
                  const SizedBox(height: 10),
                  TextField(
                    controller: columnsController,
                    decoration: const InputDecoration(
                      labelText: 'Número de columnas (m)',
                      border: OutlineInputBorder(),
                    ),
                    keyboardType: TextInputType.number,
                    enabled: mapa ==
                        null, // Bloquear entrada si hay una matriz cargada
                  ),
                  const SizedBox(height: 10),
                  TextField(
                    controller: iterationsController,
                    decoration: const InputDecoration(
                      labelText: 'Número de Niveles de Profundidad',
                      border: OutlineInputBorder(),
                    ),
                    keyboardType: TextInputType.number,
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          if (!isConfigured)
            const Text(
              'También puede cargar un archivo o continuar manualmente',
              style: TextStyle(fontSize: 16),
            ),
          if (!isConfigured) const SizedBox(height: 20),
          ElevatedButton.icon(
            onPressed: loadFile,
            icon: fileName != null
                ? const Icon(Icons.check, color: Colors.green)
                : const Icon(Icons.upload_file),
            label: Text(fileName ?? 'Cargar archivo .txt'),
          ),
          if (isReadFile) const SizedBox(height: 20),
          if (isReadFile)
            ElevatedButton(
              onPressed: resetConfiguration,
              child: const Text('Quitar archivo cargado'),
            ),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: configureGrid,
            child: const Text('Crear laberinto'),
          ),
          const SizedBox(height: 20),
        ],
      ),
    );
  }

  Future<void> _runAlgorithm() async {
    if (!validateInputs(true)) return;

    //Prueba: Imprimir los datos ingresados
    //imprimir el mapa linea por linea
    print('Mapa:$mapa');
    print('Inicio: $inicio');
    print('Meta: $meta');
    print('Niveles de profundidad: $iterations');

    setState(() {
      isLoading = true;
    });

    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5001/algorithms'),
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: json.encode({
          //mandar los datos al servidor
          'Mapa': mapa,
          'Inicio': inicio,
          'Meta': meta,
          'MaximoIteraciones': iterations,
        }),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print("Respuesta del servidor: $data");
      } else {
        print("Error en la solicitud: ${response.statusCode}");
      }
    } catch (e) {
      print("Error durante la conexión HTTP: $e");
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  void setMarker(int marker) {
    setState(() {
      selectedMarker = marker;
    });
  }

  void configureGrid() {
    if (validateInputs(false)) {
      setState(() {
        if (rowsController.text.isNotEmpty &&
            columnsController.text.isNotEmpty) {
          rows = int.parse(rowsController.text);
          columns = int.parse(columnsController.text);
        }

        iterations = int.parse(iterationsController.text);
        isConfigured = true;
      });
    }
  }

  void resetConfiguration() {
    setState(() {
      isConfigured = false;
      isReadFile = false;
      mapa = null;
      fileName = null;
      rowsController.clear();
      columnsController.clear();
      iterationsController.clear();
      isInicioSet = false;
      isMetaSet = false;
    });
  }

  bool validateInputs(preparado) {
    if (mapa == null) {
      if (rowsController.text.isEmpty || columnsController.text.isEmpty) {
        showErrorDialog('Por favor, complete todos los campos.');
        return false;
      }
      try {
        int.parse(rowsController.text);
        int.parse(columnsController.text);
      } catch (e) {
        showErrorDialog(
            'Por favor, ingrese solo números en los campos de filas y columnas.');
        return false;
      }
    }
    if (iterationsController.text.isEmpty) {
      showErrorDialog('Por favor, complete todos los campos.');
      return false;
    }
    try {
      int.parse(iterationsController.text);
    } catch (e) {
      showErrorDialog(
          'Por favor, ingrese solo números en el campo de niveles de profundidad.');
      return false;
    }
    if (isConfigured && preparado) {
      if (!isInicioSet) {
        showErrorDialog('Por favor, seleccione una salida en el laberinto.');
        return false;
      }
      if (!isMetaSet) {
        showErrorDialog('Por favor, seleccione una meta en el laberinto.');
        return false;
      }
    }

    return true;
  }

  void showErrorDialog(String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Error'),
          content: Text(message),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('OK'),
            ),
          ],
        );
      },
    );
  }

  Future<void> loadFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['txt'],
    );

    if (result != null) {
      File file = File(result.files.single.path!);
      List<String> lines = await file.readAsLines();
      List<List<String>> tempmapa =
          lines.map((line) => line.split('')).toList();

      setState(() {
        rows = tempmapa.length;
        columns = tempmapa[0].length;
        fileName = result.files.single.name;
        rowsController.text = rows.toString();
        columnsController.text = columns.toString();
        isReadFile = true;
      });

      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('¿Deseas usar esta mapa?'),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                for (var row in tempmapa)
                  Text(row.map((e) => "'$e'").toList().toString()),
              ],
            ),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: const Text('Cancelar'),
              ),
              TextButton(
                onPressed: () {
                  setState(() {
                    mapa = tempmapa;
                  });
                  Navigator.of(context).pop();
                },
                child: const Text('Confirmar'),
              ),
            ],
          );
        },
      );
    }
  }
}

class FooterWidget extends StatelessWidget {
  const FooterWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      width: MediaQuery.of(context).size.width,
      color: const Color.fromARGB(255, 255, 255, 255),
      child: const Text(
        '© 2023 Agent Mouse. Todos los derechos reservados.',
        style: TextStyle(fontSize: 14),
        textAlign: TextAlign.center,
      ),
    );
  }
}
