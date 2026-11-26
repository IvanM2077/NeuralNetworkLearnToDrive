# 🚗 Simulador de Conducción con Inteligencia Artificial

Aplicación interactiva en Python que combina una simulación 2D en **Pygame** con modelos de **Machine Learning / Deep Learning** acelerados por GPU para entrenar un coche autónomo en una pista.

## 🛠️ Tecnologías y Requisitos

- **Python:** `3.10.11`
- **Simulación y Gráficos:** `pygame`
- **Cálculo y Datos:** `numpy`, `pandas`
- **Deep Learning (GPU):** `torch` (PyTorch con soporte CUDA)
- **Visualización de Métricas:** `matplotlib` _(recomendado para graficar el aprendizaje)_

---

## 📁 Estructura del Proyecto

```text
project/
│
├── assets/                     # Imágenes (sprites de coches, pistas, iconos)
├── saved_models/               # Modelos entrenados (.pth) y logs de datos (.csv)
│
├── Graphics/                   # Todo lo relacionado con el renderizado visual
│   ├── __init__.py
│   ├── Window.py               # Configuración de ventana, FPS y bucle visual
│   ├── Coche.py                # Clase del vehículo (física, sensores, dibujo)
│   ├── Pista.py                # Carga de pista, colisiones y checkpoints
│   └── Botones.py              # Interfaz de usuario (pausa, reiniciar, cambiar modo)
│
├── ML/                         # Inteligencia Artificial y entrenamiento
│   ├── __init__.py
│   └── NNCN.py                 # Arquitectura de la red neuronal y lógica de GPU
│
├── Controles/                  # Desacoplamiento de cómo se maneja el coche
│   ├── __init__.py
│   ├── manual.py               # Control por teclado (para pruebas o recolectar datos)
│   └── ia_controller.py        # Control autónomo usando las predicciones de ML/
│
├── config.py                   # Constantes globales (resolución, FPS, hiperparámetros)
├── main.py                     # Punto de entrada principal de la aplicación
├── requirements.txt            # Lista de dependencias del proyecto
└── README.md                   # Documentación del proyecto
```
