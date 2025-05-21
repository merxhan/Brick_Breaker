# 🧱 Juego Rompe Bloques con Control por Mano (Pygame + Mediapipe)

Este es un proyecto interactivo de un juego tipo "Arkanoid"/"Breakout" desarrollado con Python, que utiliza visión computacional para controlar la barra del jugador con el movimiento de la mano detectado por la cámara.

## 🎮 Características

- Control de la barra usando el dedo índice (con cámara web).
- Interfaz visual con fondo en tiempo real desde la webcam.
- Gráficos con Pygame y detección de mano con Mediapipe.
- Detección de colisiones con bloques, barra y paredes.
- Sistema de puntaje con reinicio tras Game Over.

## 📸 Captura de pantalla

![Game.png](img/Game.png)

## ⚙️ Requisitos

- Python 3.10
- Cámara web activa

Instalación de dependencias:

```bash
  pip install -r requirements.txt
```

## 📁 Estructura del Proyecto

    Brick_Breaker/
    ├── main.py
    ├── requirements.txt
    ├── img/
    │   ├── bar.png
    │   ├── ball.png
    │   └── brick.png
    └── README.md

## ▶️ Ejecución

```bash
  python main.py
```

# 🎮 Controles del Juego

- Dedo Índice (mano derecha): mueve la barra.
- ESC: salir del juego.
- ENTER: reiniciar después del “Game Over”.

## 📊 Mecánicas
- Cada bloque roto suma 10 puntos.
- El juego termina si la pelota toca el fondo.
- Puedes reiniciar el juego presionando ENTER.

## 🔮 Ideas Futuras
- Soporte para múltiples niveles.
- Detección de gestos para activar habilidades.
- Mejora visual con efectos animados y sonido.
- Ranking local de puntajes máximos.

## 📜 Licencia

Este proyecto es de código abierto y puede ser modificado y distribuido bajo los términos de la licencia MIT.

