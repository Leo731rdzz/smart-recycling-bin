# Leonardo Rodríguez

from arduino.app_utils import App, Bridge
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection
from datetime import datetime, UTC
import time
import threading

ui = WebUI()
detection_stream = VideoObjectDetection(confidence=0.5, debounce_sec=0.5)
ui.on_message("override_th", lambda sid, threshold: detection_stream.override_threshold(threshold))

classes = ["apple", "plastic", "paper", "pet", "can", "egg"]

stable_counts    = {cls: 0 for cls in classes}
last_action_time = {cls: 0 for cls in classes}
in_progress      = {cls: False for cls in classes}

COOLDOWN_NORMAL = 8.0
COOLDOWN_CAN    = 10.0

# Función independiente para manejar el hardware sin congelar la cámara
def ejecutar_accion_fisica(cls):
    global in_progress
    try:
        audio_map = {
            "apple": 1,
            "pet": 2,
            "can": 3,
            "paper": 4,
            "egg": 5,
            "plastic": 6
        }
        
        if cls in audio_map:
            Bridge.call("play_audio", audio_map[cls])
            time.sleep(1.5) 
        
        if cls in ["paper", "apple", "egg"]:
            Bridge.call("set_servo", 0)
            time.sleep(3.5)
            Bridge.call("set_servo", 90)
        elif cls in ["plastic", "pet"]:
            Bridge.call("set_servo", 180)
            time.sleep(3.5)
            Bridge.call("set_servo", 90)
        elif cls == "can":
            Bridge.call("buzz", 2000)
            time.sleep(3.5)

    except Exception as e:
        print(f"Error de Bridge para {cls}: {e}")
    finally:
        # Liberamos el estado de progreso pase lo que pase
        in_progress[cls] = False

def send_detections_to_ui(detections: dict):
    global stable_counts, last_action_time, in_progress

    detected_this_frame = {cls: 0.0 for cls in classes}
    now = time.time()

    for key, values in detections.items():
        for value in values:
            entry = {
                "content": key,
                "confidence": value.get("confidence"),
                "timestamp": datetime.now(UTC).isoformat()
            }
            ui.send_message("detection", message=entry)

        if key in classes:
            max_conf = max(v.get("confidence", 0.0) for v in values)
            detected_this_frame[key] = max_conf

    # Umbrales que controlan qué tan seguro debe estar el modelo para actuar
    CONF_THRESHOLD = 0.82
    CAN_THRESHOLD  = 0.88
    STABLE_FRAMES  = 2

    for cls in classes:
        conf = detected_this_frame[cls]
        cooldown = COOLDOWN_CAN if cls == "can" else COOLDOWN_NORMAL

        if conf >= (CAN_THRESHOLD if cls == "can" else CONF_THRESHOLD):
            stable_counts[cls] += 1
        else:
            stable_counts[cls] = 0

        # Si supera los filtros de estabilidad, lanzamos el hilo en segundo plano
        if stable_counts[cls] >= STABLE_FRAMES and not in_progress[cls] and (now - last_action_time[cls] > cooldown):
            in_progress[cls] = True
            last_action_time[cls] = now
            
            # Iniciamos la acción física sin bloquear el video
            threading.Thread(target=ejecutar_accion_fisica, args=(cls,), daemon=True).start()

detection_stream.on_detect_all(send_detections_to_ui)
App.run()
