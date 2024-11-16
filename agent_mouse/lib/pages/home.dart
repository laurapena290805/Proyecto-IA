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
            '¡Bienvenido a Agent Mouse! Ayuda al ratón a encontrar el queso en el laberinto. Selecciona el algoritmo que deseas utilizar y presiona el botón de inicio para comenzar la búsqueda.',
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
  // ignore: library_private_types_in_public_api
  _CentralContainerState createState() => _CentralContainerState();
}

class _CentralContainerState extends State<CentralContainer> {
  int selectedMarker = 1;
  String algoritmoSeleccionado = 'limitada_profundidad';
  late ButtonState buttonState;
  bool isLoading = false;
  bool isConfigured = false;
  int rows = 0;
  int columns = 0;
  int iterations = 0;
  int depth = 0;
  List<List<String>>? matriz;
  String? fileName;
  String algoritmoActual = '';

  final TextEditingController rowsController = TextEditingController();
  final TextEditingController columnsController = TextEditingController();
  final TextEditingController iterationsController = TextEditingController();
  final TextEditingController depthController = TextEditingController();
  final TextEditingController salidaController = TextEditingController();
  final TextEditingController metaController = TextEditingController();

  void setMarker(int marker) {
    setState(() {
      selectedMarker = marker;
    });
  }

  void configureGrid() {
    if (validateInputs()) {
      setState(() {
        if (rowsController.text.isNotEmpty &&
            columnsController.text.isNotEmpty) {
          rows = int.parse(rowsController.text);
          columns = int.parse(columnsController.text);
        }

        iterations = int.parse(iterationsController.text);
        depth = int.parse(depthController.text);
        isConfigured = true;
      });
    }
  }

  bool validateInputs() {
    if (matriz == null) {
      if (rowsController.text.isEmpty || columnsController.text.isEmpty) {
        showErrorDialog('Por favor, complete todos los campos.');
        return false;
      }
    } else {
      if (salidaController.text.isEmpty || metaController.text.isEmpty) {
        showErrorDialog('Por favor, complete todos los campos.');
        return false;
      }
      if (!RegExp(r'^\d+,\d+$').hasMatch(salidaController.text) ||
          !RegExp(r'^\d+,\d+$').hasMatch(metaController.text)) {
        showErrorDialog('Las coordenadas deben tener el formato x,y.');
        return false;
      }
    }
    if (iterationsController.text.isEmpty || depthController.text.isEmpty) {
      showErrorDialog('Por favor, complete todos los campos.');
      return false;
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
      List<List<String>> tempMatriz =
          lines.map((line) => line.split('')).toList();

      setState(() {
        rows = tempMatriz.length;
        columns = tempMatriz[0].length;
        fileName = result.files.single.name;
      });

      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('¿Deseas usar esta matriz?'),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                for (var row in tempMatriz)
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
                    matriz = tempMatriz;
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

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 50),
      color: const Color.fromARGB(255, 255, 255, 255),
      child: Column(
        children: [
          const SizedBox(height: 20),

          //CONTENIDO DE CONFIGURACION
          if (!isConfigured)
            Column(
              children: [
                Text(
                  matriz != null
                      ? 'Ingrese las coordenadas para la matriz seleccionada'
                      : 'Configura a tu ratón ingresando los siguientes datos',
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20),
                if (matriz == null) ...[
                  TextField(
                    controller: rowsController,
                    decoration: const InputDecoration(
                      labelText: 'Número de filas (n)',
                      border: OutlineInputBorder(),
                    ),
                    keyboardType: TextInputType.number,
                  ),
                  const SizedBox(height: 10),
                  TextField(
                    controller: columnsController,
                    decoration: const InputDecoration(
                      labelText: 'Número de columnas (m)',
                      border: OutlineInputBorder(),
                    ),
                    keyboardType: TextInputType.number,
                  ),
                ] else ...[
                  TextField(
                    controller: salidaController,
                    decoration: const InputDecoration(
                      labelText: 'Coordenadas de salida (x,y)',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 10),
                  TextField(
                    controller: metaController,
                    decoration: const InputDecoration(
                      labelText: 'Coordenadas de meta (x,y)',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ],
                const SizedBox(height: 10),
                TextField(
                  controller: iterationsController,
                  decoration: const InputDecoration(
                    labelText: 'Número de iteraciones',
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.number,
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: depthController,
                  decoration: const InputDecoration(
                    labelText: 'Número de profundidad',
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.number,
                ),
                const SizedBox(height: 20),
                const Text(
                  'También puede cargar un archivo',
                  style: TextStyle(fontSize: 16),
                ),
                const SizedBox(height: 10),
                ElevatedButton.icon(
                  onPressed: loadFile,
                  icon: fileName != null
                      ? const Icon(Icons.check, color: Colors.green)
                      : const Icon(Icons.upload_file),
                  label: Text(fileName ?? 'Cargar archivo .txt'),
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: configureGrid,
                  child: const Text('Continuar'),
                ),
              ],
            ),
          const SizedBox(height: 20),
          if (isConfigured)

            //CONTENIDO DE EJECUCION
            Column(
              children: [
                Row(
                  children: [
                    Expanded(
                      child: Container(
                        width: MediaQuery.of(context).size.width * 0.8,
                        height: MediaQuery.of(context).size.height * 0.6,
                        decoration: const BoxDecoration(
                          borderRadius: BorderRadius.all(Radius.circular(20)),
                          color: Color.fromARGB(75, 179, 179, 179),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(20),
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(20),
                            child: Image.asset(
                              'lib/assets/arbol.png',
                              fit: BoxFit.cover,
                            ),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 20),
                    Expanded(
                      child: Container(
                        width: MediaQuery.of(context).size.width * 0.8,
                        height: MediaQuery.of(context).size.height * 0.6,
                        decoration: const BoxDecoration(
                          color: Color.fromARGB(75, 179, 179, 179),
                        ),
                        child: ButtonGrid(
                          rows: rows,
                          columns: columns,
                          selectedMarker: selectedMarker,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 20),
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
                      ElevatedButton(
                        onPressed: _runAlgorithm,
                        child: const Text('Iniciar',
                            style: AppStyles.buttonTextStyle),
                      ),
                      const SizedBox(height: 20),
                      Text(
                        'Algoritmo actual: $algoritmoActual',
                        style: AppStyles.infomationTextStyle,
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),
              ],
            ),
        ],
      ),
    );
  }

  Future<void> _runAlgorithm() async {
    setState(() {
      isLoading = true;
    });

    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5000/algorithms'),
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: json.encode({
          'Inicio': [0, 2], // Ejemplo de coordenadas de inicio
          'Meta': [1, 3], // Ejemplo de coordenadas de meta
          'Mapa': [
            ['.', '.', '.', '.'],
            ['.', '#', '#', '.'],
            ['.', '#', '.', '.'],
            ['.', '.', '.', '#'],
          ], // Ejemplo de mapa
          'MaximoIteraciones': 2,
        }),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print(data);
        setState(() {
          print("Si se pudo ${data['confirmacion']} ");
        });
      } else {
        setState(() {
          // Handle error
        });
      }
    } catch (e) {
      setState(() {
        // Handle error
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
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
