// ignore: file_names
import 'package:flutter/material.dart';

class ButtonGrid extends StatefulWidget {
  final int rows;
  final int columns;
  final int selectedMarker; // Marcador seleccionado

  const ButtonGrid({
    super.key,
    required this.rows,
    required this.columns,
    required this.selectedMarker,
  });

  @override
  // ignore: library_private_types_in_public_api
  _ButtonGridState createState() => _ButtonGridState();
}

class _ButtonGridState extends State<ButtonGrid> {
  late ButtonState buttonState; // Nueva instancia de ButtonState
  late List<List<int>> mapa; // Matriz de estados para cada botón

  // Coordenadas de los botones azul y verde
  String inicioCoor = '(x, y)';
  String metaXY = '(x, y)';

  @override
  void initState() {
    super.initState();
    buttonState = ButtonState(rows: widget.rows, columns: widget.columns);
    mapa = List.generate(
        widget.rows, (_) => List.generate(widget.columns, (_) => 0));
  }

  void markButton(int row, int col) {
    int buttonIndex = row * widget.columns + col;

    setState(() {
      // Actualizamos la matriz de visualización
      if (widget.selectedMarker == 3) {
        mapa[row][col] = mapa[row][col] == 3 ? 0 : 3;
        buttonState.updatemapaBotones(
            row, col, mapa[row][col] == 3 ? '#' : '.');
      } else if (widget.selectedMarker == 1) {
        if (buttonState.getinicioCoor != null) {
          int oldRow = buttonState.getinicioCoor! ~/ widget.columns;
          int oldCol = buttonState.getinicioCoor! % widget.columns;
          mapa[oldRow][oldCol] = 0;
          buttonState.updatemapaBotones(oldRow, oldCol, '.');
        }
        mapa[row][col] = 1;
        buttonState.updatemapaBotones(row, col, '.');
        buttonState.updateinicioCoor(buttonIndex);
        inicioCoor = '(${row + 1}, ${col + 1})';
      } else if (widget.selectedMarker == 2) {
        if (buttonState.getmetaCoor != null) {
          int oldRow = buttonState.getmetaCoor! ~/ widget.columns;
          int oldCol = buttonState.getmetaCoor! % widget.columns;
          mapa[oldRow][oldCol] = 0;
          buttonState.updatemapaBotones(oldRow, oldCol, '.');
        }
        mapa[row][col] = 2;
        buttonState.updatemapaBotones(row, col, '.');
        buttonState.updatemetaCoor(buttonIndex);
        metaXY = '(${row + 1}, ${col + 1})';
      }

      // Imprimir la matriz en la consola (para depuración)
      print('Matriz de visualización:');
      print(buttonState.getmapaBotones);
      print('Coordenadas de salida: $inicioCoor');
      print('Coordenadas de la meta: $metaXY');
    });
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        double buttonWidth = constraints.maxWidth / widget.columns;
        double buttonHeight = constraints.maxHeight / widget.rows;

        return GridView.builder(
          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: widget.columns,
            childAspectRatio: buttonWidth / buttonHeight,
          ),
          itemCount: widget.rows * widget.columns,
          itemBuilder: (context, index) {
            int row = index ~/ widget.columns;
            int col = index % widget.columns;

            Color buttonColor;
            Widget buttonContent;
            switch (mapa[row][col]) {
              case 1:
                buttonColor = Colors.blue;
                buttonContent = const Icon(Icons.circle, color: Colors.white);
                break;
              case 2:
                buttonColor = Colors.green;
                buttonContent = const Icon(Icons.check, color: Colors.white);
                break;
              case 3:
                buttonColor = Colors.red;
                buttonContent = const Icon(Icons.close, color: Colors.white);
                break;
              default:
                buttonColor = const Color.fromARGB(115, 132, 158, 155);
                buttonContent = const SizedBox.shrink();
            }

            return GestureDetector(
              onTap: () => markButton(row, col),
              child: Container(
                margin: const EdgeInsets.all(2),
                decoration: BoxDecoration(
                  color: buttonColor,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Center(child: buttonContent),
              ),
            );
          },
        );
      },
    );
  }
}

class ButtonState {
  List<List<String>>
      mapaBotones; // Matriz de caracteres para la visualización
  int? inicioCoor;
  int? metaCoor;

  ButtonState({
    required int rows,
    required int columns,
  })  : mapaBotones =
            List.generate(rows, (_) => List.generate(columns, (_) => '.')),
        inicioCoor = null,
        metaCoor = null;

  // Getters
  List<List<String>> get getmapaBotones => mapaBotones;
  int? get getinicioCoor => inicioCoor;
  int? get getmetaCoor => metaCoor;

  // Métodos para actualizar índices y matriz
  void updateinicioCoor(int index) {
    inicioCoor = index;
  }

  void updatemetaCoor(int index) {
    metaCoor = index;
  }

  void updatemapaBotones(int row, int col, String value) {
    mapaBotones[row][col] = value;
  }
}
