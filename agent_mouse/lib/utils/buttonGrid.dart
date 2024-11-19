import 'package:flutter/material.dart';

class ButtonGrid extends StatefulWidget {
  final int rows;
  final int columns;
  final int selectedMarker;
  final List<List<String>>? matrizCargada;
  final Function(int, int)? onUpdateInicio; // Nuevo callback
  final Function(int, int)? onUpdateMeta; // Nuevo callback
  final Function(List<List<String>>)? onUpdateMatriz; // Nuevo callback

  const ButtonGrid({
    super.key,
    required this.rows,
    required this.columns,
    required this.selectedMarker,
    this.matrizCargada,
    this.onUpdateInicio,
    this.onUpdateMeta,
    this.onUpdateMatriz,
  });

  @override
  State<ButtonGrid> createState() => _ButtonGridState();
}

class _ButtonGridState extends State<ButtonGrid> {
  late ButtonState buttonState;
  late List<List<int>> mapa;

  String inicioCoor = '(x, y)';
  String metaXY = '(x, y)';

  @override
  void initState() {
    super.initState();
    buttonState = ButtonState(rows: widget.rows, columns: widget.columns);
    mapa = List.generate(
        widget.rows, (_) => List.generate(widget.columns, (_) => 0));

    // Inicializar el grid basado en matrizCargada
    if (widget.matrizCargada != null) {
      for (int i = 0; i < widget.rows; i++) {
        for (int j = 0; j < widget.columns; j++) {
          if (widget.matrizCargada![i][j] == '#') {
            mapa[i][j] = 3; // Marcar como bloqueado
            buttonState.updatemapaBotones(i, j, '#');
          }
        }
      }
    }
  }

  void markButton(int row, int col) {
    int buttonIndex = row * widget.columns + col;

    setState(() {
      if (widget.selectedMarker == 3) {
        mapa[row][col] = mapa[row][col] == 3 ? 0 : 3;
        buttonState.updatemapaBotones(
            row, col, mapa[row][col] == 3 ? '#' : '.');
        if (widget.onUpdateMatriz != null) {
          widget.onUpdateMatriz!(buttonState.getmapaBotones);
        }
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
        if (widget.onUpdateInicio != null) {
          widget.onUpdateInicio!(row, col);
        }
        if (widget.onUpdateMatriz != null) {
          widget.onUpdateMatriz!(buttonState.getmapaBotones);
        }
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
        if (widget.onUpdateMeta != null) {
          widget.onUpdateMeta!(row, col);
        }
        if (widget.onUpdateMatriz != null) {
          widget.onUpdateMatriz!(buttonState.getmapaBotones);
        }
      }

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
  List<List<String>> mapaBotones;
  int? inicioCoor;
  int? metaCoor;

  ButtonState({
    required int rows,
    required int columns,
  })  : mapaBotones =
            List.generate(rows, (_) => List.generate(columns, (_) => '.')),
        inicioCoor = null,
        metaCoor = null;

  List<List<String>> get getmapaBotones => mapaBotones;
  int? get getinicioCoor => inicioCoor;
  int? get getmetaCoor => metaCoor;

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
