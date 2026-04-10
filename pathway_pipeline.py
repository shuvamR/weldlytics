# pathway_pipeline.py
import time
import threading
import queue
import numpy as np
from datetime import datetime
from bdh_model import predict_quality, training_accuracy, days_trained

data_queue = queue.Queue()

# Consumable tracking
electrode_usage = 1000  # mm remaining
gas_remaining = 85  # % remaining
total_welds = 0
bad_welds = 0
material_saved = 0
rework_saved = 0
defects_prevented = 0


def esp32_simulator():
    """Simulate ESP32 sending welding data every 0.5 seconds."""
    global electrode_usage, gas_remaining, total_welds, bad_welds
    global material_saved, rework_saved, defects_prevented

    buffer = []
    consecutive_bad = 0

    while True:
        # Simulate current
        if np.random.rand() < 0.1:
            if np.random.rand() > 0.5:
                current = np.random.normal(170, 15)
            else:
                current = np.random.normal(40, 10)
        else:
            current = np.random.normal(100, 20)

        temperature = 40 + (current - 100) * 0.2 + np.random.normal(0, 2)
        vibration = 0.5 + abs(current - 100) * 0.02 + np.random.normal(0, 0.1)

        timestamp = datetime.now()
        buffer.append(current)
        if len(buffer) > 10:
            buffer.pop(0)

        quality, confidence, explanation, suggestion = predict_quality(buffer)

        # Update metrics
        total_welds += 1
        electrode_usage -= np.random.uniform(0.5, 2)
        gas_remaining -= np.random.uniform(0.1, 0.5)

        if quality == "REJECTED":
            bad_welds += 1
            consecutive_bad += 1
            defects_prevented += 1
            material_saved += np.random.uniform(5, 15)
            rework_saved += np.random.uniform(10, 30)
        else:
            consecutive_bad = 0

        # Alert levels
        if quality == "REJECTED" and confidence > 0.7:
            severity = "HIGH"
        elif quality == "REJECTED":
            severity = "MEDIUM"
        else:
            severity = "LOW"

        # Machine risk detection
        machine_risk = "LOW"
        if temperature > 80:
            machine_risk = "HIGH"
        elif temperature > 65:
            machine_risk = "MEDIUM"

        data_queue.put({
            'timestamp': timestamp,
            'current': current,
            'temperature': temperature,
            'vibration': vibration,
            'quality': quality,
            'confidence': confidence,
            'explanation': explanation,
            'suggestion': suggestion,
            'severity': severity,
            'machine_risk': machine_risk,
            'buffer': buffer.copy(),
            'electrode_usage': max(0, electrode_usage),
            'gas_remaining': max(0, gas_remaining),
            'total_welds': total_welds,
            'bad_welds': bad_welds,
            'defects_prevented': defects_prevented,
            'material_saved': material_saved,
            'rework_saved': rework_saved,
            'training_accuracy': training_accuracy,
            'days_trained': days_trained
        })

        # Low stock alerts
        if electrode_usage < 100:
            data_queue.put({'alert': 'LOW_ELECTRODE', 'message': ' Electrode low - Replace soon'})
        if gas_remaining < 15:
            data_queue.put({'alert': 'LOW_GAS', 'message': ' Gas low - Refill cylinder'})

        time.sleep(0.5)


sim_thread = threading.Thread(target=esp32_simulator, daemon=True)
sim_thread.start()

if __name__ == "__main__":
    print("Weldlytics Pipeline Running...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped.")