import 'package:flutter/material.dart';

class ButtonGrid extends StatefulWidget {
  final int rows;
  final int columns;
  final int selectedMarker;

  const ButtonGrid({
    super.key,
    required this.rows,
    required this.columns,
    required this.selectedMarker,
  });

  @override
  _ButtonGridState createState() => _ButtonGridState();

  // Getters públicos para acceder a las variables desde otros archivos
  List<List<String>> get displayMatrix => _ButtonGridState.instance?.displayMatrix ?? [];
  List? get blueButtonIndex => _ButtonGridState.instance?.blueCoordinates;
  List? get greenButtonIndex => _ButtonGridState.instance?.greenCoordinates;
}

class _ButtonGridState extends State<ButtonGrid> {
  // Instancia estática para acceder a los valores desde los getters
  static _ButtonGridState? instance;

  late List<List<int>> buttonStates;
  late List<List<String>> displayMatrix;
  int? blueButtonIndex;
  int? greenButtonIndex;

  List blueCoordinates = [0 , 0];
  List greenCoordinates = [0 , 0];

  @override
  void initState() {
    super.initState();
    instance = this; // Asignamos la instancia actual a la variable estática
    buttonStates = List.generate(widget.rows, (_) => List.generate(widget.columns, (_) => 0));
    displayMatrix = List.generate(widget.rows, (_) => List.generate(widget.columns, (_) => '.'));
  }

  void markButton(int row, int col) {
    int buttonIndex = row * widget.columns + col;

    setState(() {
      if (widget.selectedMarker == 3) {
        buttonStates[row][col] = buttonStates[row][col] == 3 ? 0 : 3;
        displayMatrix[row][col] = buttonStates[row][col] == 3 ? '#' : '.';
      } else if (widget.selectedMarker == 1) {
        if (blueButtonIndex != null) {
          int oldRow = blueButtonIndex! ~/ widget.columns;
          int oldCol = blueButtonIndex! % widget.columns;
          buttonStates[oldRow][oldCol] = 0;
          displayMatrix[oldRow][oldCol] = '.';
        }
        buttonStates[row][col] = 1;
        displayMatrix[row][col] = '.';
        blueButtonIndex = buttonIndex;
        blueCoordinates[0] = row;
        blueCoordinates[1] = col;
      } else if (widget.selectedMarker == 2) {
        if (greenButtonIndex != null) {
          int oldRow = greenButtonIndex! ~/ widget.columns;
          int oldCol = greenButtonIndex! % widget.columns;
          buttonStates[oldRow][oldCol] = 0;
          displayMatrix[oldRow][oldCol] = '.';
        }
        buttonStates[row][col] = 2;
        displayMatrix[row][col] = '.';
        greenButtonIndex = buttonIndex;
        greenCoordinates[0] = row;
        greenCoordinates[1] = col;
      }

      print('Matriz de visualización:');
      print(displayMatrix);
      print('Coordenadas de salida: $blueCoordinates');
      print('Coordenadas de la meta: $greenCoordinates');
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
            switch (buttonStates[row][col]) {
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
