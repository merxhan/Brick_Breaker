import pygame  # Motor de gráficos y control de eventos
import cv2  # Captura de vídeo desde la cámara
import mediapipe as mp  # Detección de mano con inteligencia artificial
import numpy as np  # Manipulación de arrays y procesamiento de imágenes
import sys  # Proporciona acceso a funciones del sistema (como salir del programa)

# Inicializar librerías
pygame.init()  # Inicializa todos los módulos de pygame
mp_hands = mp.solutions.hands  # Crea una referencia al módulo de manos de Mediapipe
mp_draw = mp.solutions.drawing_utils  # Utilidades de dibujo para los landmarks de las manos

# Constantes de ventana
WIDTH, HEIGHT = 1000, 800  # Dimensiones de la ventana del juego
FPS = 30  # Cuadros por segundo del juego

# Crear ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Crea la ventana principal del juego
pygame.display.set_caption("Juego rompe Bloques")  # Establece el título de la ventana
clock = pygame.time.Clock()  # Crea un reloj para controlar el tiempo de actualización
font = pygame.font.SysFont("Arial", 36)  # Fuente para mostrar texto (como puntaje)

# Cargar imágenes y ajustar tamaños
paddle_image = pygame.transform.scale(pygame.image.load('img/bar.png'), (150, 40))  # Carga y escala la imagen de la barra
ball_image = pygame.transform.scale(pygame.image.load('img/ball.png'), (40, 40))  # Carga y escala la imagen de la pelota
brick_img_original = pygame.image.load('img/brick.png')  # Carga la imagen original del bloque

# Parámetros de paddle
paddle_width, paddle_height = 150, 40  # Ancho y alto de la barra
paddle_x, paddle_y = WIDTH // 2 - paddle_width // 2, HEIGHT - 60  # Posición inicial de la barra centrada

# Parámetros de pelota
ball_radius = 20  # Radio de la pelota
ball_x, ball_y = WIDTH // 2, HEIGHT // 2  # Posición inicial de la pelota
ball_speed_x, ball_speed_y = 8, 8  # Velocidad de la pelota en X y Y

# Crear bloques
block_rows, block_columns = 4, 10  # Cantidad de filas y columnas de bloques
block_width, block_height = WIDTH // block_columns, 50  # Tamaño de cada bloque
block_image = pygame.transform.scale(brick_img_original, (block_width, block_height))  # Escala la imagen de bloque

def crear_bloques():  # Función para crear la lista de bloques
    return [  # Devuelve una lista de rectángulos que representan cada bloque
        pygame.Rect(col * block_width, row * block_height, block_width, block_height)  # Crea un bloque por posición
        for row in range(block_rows)  # Itera por filas
        for col in range(block_columns)  # Itera por columnas
    ]

blocks = crear_bloques()  # Genera la lista inicial de bloques
score = 0  # Inicializa el puntaje
game_over = False  # Bandera que indica si el juego ha terminado

# Inicializar cámara
cap = cv2.VideoCapture(0)  # Inicia la cámara (0 es la predeterminada)

# Detección de manos con contexto seguro
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1) as hands:  # Modelo de detección

    while True:  # Bucle principal del juego
        for event in pygame.event.get():  # Revisa los eventos del sistema
            if event.type == pygame.QUIT:  # Si se intenta cerrar la ventana
                cap.release()  # Libera la cámara
                pygame.quit()  # Cierra pygame
                sys.exit()  # Finaliza el programa
            elif event.type == pygame.KEYDOWN:  # Si se presiona una tecla
                if event.key == pygame.K_ESCAPE:  # Si se presiona ESC
                    cap.release()
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN and game_over:  # Si se presiona ENTER después del Game Over
                    # Reiniciar el juego
                    paddle_x = WIDTH // 2 - paddle_width // 2  # Restablecer posición de barra
                    ball_x, ball_y = WIDTH // 2, HEIGHT // 2  # Restablecer posición de pelota
                    ball_speed_x, ball_speed_y = 8, 8  # Restablecer velocidad
                    blocks = crear_bloques()  # Recrear bloques
                    score = 0  # Reiniciar puntaje
                    game_over = False  # Reiniciar estado de juego

        # Leer frame de cámara
        ret, frame = cap.read()  # Captura un frame de la cámara
        if not ret:  # Si no se obtiene imagen
            break  # Termina el bucle

        frame = cv2.flip(frame, 1)  # Espeja la imagen (efecto espejo)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convierte de BGR (OpenCV) a RGB (Mediapipe)
        results = hands.process(rgb_frame)  # Procesa el frame para detectar manos

        if results.multi_hand_landmarks:  # Si hay manos detectadas
            for hand_landmarks in results.multi_hand_landmarks:  # Recorre las manos detectadas
                index_finger = hand_landmarks.landmark[8]  # Obtiene la coordenada del dedo índice
                paddle_x = int(index_finger.x * WIDTH) - paddle_width // 2  # Mueve la barra con la mano
                mp_draw.draw_landmarks(rgb_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)  # Dibuja los puntos de la mano

        # Límite de paddle
        paddle_x = max(0, min(WIDTH - paddle_width, paddle_x))  # Limita el movimiento de la barra dentro de la pantalla

        if not game_over:  # Si el juego está en curso
            # Movimiento de pelota
            ball_x += ball_speed_x  # Actualiza posición en X
            ball_y += ball_speed_y  # Actualiza posición en Y

            # Colisiones con paredes
            if ball_x - ball_radius < 0 or ball_x + ball_radius > WIDTH:  # Rebote lateral
                ball_speed_x *= -1
            if ball_y - ball_radius < 0:  # Rebote superior
                ball_speed_y *= -1
            if ball_y + ball_radius > HEIGHT:  # Si toca el fondo (pierde)
                game_over = True

            # Colisión con paddle
            if paddle_x < ball_x < paddle_x + paddle_width and paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height:
                ball_speed_y *= -1  # Rebote en la barra

            # Colisión con bloques
            for block in blocks:  # Revisa cada bloque
                if block.collidepoint(ball_x, ball_y):  # Si hay colisión con la pelota
                    blocks.remove(block)  # Elimina el bloque
                    ball_speed_y *= -1  # Rebote
                    score += 10  # Aumenta el puntaje
                    break  # Sale del bucle de bloques

        # Mostrar cámara como fondo
        rgb_frame = cv2.resize(rgb_frame, (WIDTH, HEIGHT))  # Redimensiona el frame
        rgb_frame = np.rot90(rgb_frame)  # Rota la imagen para Pygame
        surface = pygame.surfarray.make_surface(rgb_frame)  # Convierte a Surface de Pygame
        screen.blit(surface, (0, 0))  # Dibuja el fondo

        # Dibujar paddle y pelota
        screen.blit(paddle_image, (paddle_x, paddle_y))  # Dibuja la barra
        screen.blit(ball_image, (ball_x - ball_radius, ball_y - ball_radius))  # Dibuja la pelota

        # Dibujar bloques
        for block in blocks:
            screen.blit(block_image, (block.x, block.y))  # Dibuja cada bloque

        # Mostrar puntaje
        score_text = font.render(f"Pontos: {score}", True, (255, 255, 255))  # Renderiza el texto del puntaje
        screen.blit(score_text, (20, HEIGHT - 40))  # Muestra el puntaje en pantalla

        # Mostrar mensaje de Game Over
        if game_over:
            text = font.render("Game Over - Pressione ENTER", True, (255, 0, 0))  # Renderiza mensaje
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))  # Centra el mensaje en pantalla

        pygame.display.flip()  # Actualiza la pantalla con todos los cambios
        clock.tick(FPS)  # Espera para mantener la velocidad de actualización (FPS)