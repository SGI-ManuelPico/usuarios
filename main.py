import logging
from sincronizador import sincronizarTodo

# Configuración del log
logging.basicConfig(
    filename='sincronizacion.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Mensaje inicial
logging.info("Inicio del proceso de sincronización...")

try:
    # Llama a la función de sincronización
    sincronizarTodo()
    logging.info("Sincronización completada con éxito.")
except Exception as e:
    logging.error(f"Error durante la sincronización: {e}")

# Mensaje final
logging.info("Fin del proceso.")
