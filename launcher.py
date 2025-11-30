import pyrealsense2 as rs
import numpy as np
import csv
import os
import sys
import time

# Funzione per acquisire e salvare i dati
def capture_and_save_data(pipeline, name):
    # Attende i frame dalla pipeline
    frames = pipeline.wait_for_frames()
    csv_dir = os.path.join(os.getcwd(), "Realsense CSV", name)
    # Crea la directory per i CSV se non esiste
    os.makedirs(csv_dir, exist_ok=True)
    for frame_type in ["depth", "color", "accel", "gyro"]:
        frame = get_frame_by_type(frames, frame_type)
        if frame:
            data, labels = data_to_capture(frame, frame_type)
            csv_filename = os.path.join(csv_dir, f"{name} {frame_type} data.csv")
            save_to_csv(csv_filename, data, labels)

# Funzione per estrarre dati rilevanti da un frame
def data_to_capture(frame, frame_type):
    data = np.asarray(frame.get_data())
    timestamp = frame.get_timestamp()
    formatted_timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime(timestamp / 1000.0)) + "_{:03d}".format(int(timestamp % 1000))
    number = frame.get_frame_number()
    min_distance = np.min(data)
    mean_distance = round(np.mean(data), 2)
    max_distance = np.max(data)
    labels = ["Timestamp", "Numero frame", "Distanza minima", "Distanza media", "Distanza massima"]

    if frame_type in ["depth", "color"]:
        bits = frame.get_bits_per_pixel()
        bytes_n = frame.get_bytes_per_pixel()
        width = frame.get_width()
        height = frame.get_height()
        stride = frame.get_stride_in_bytes()
        data_list = [formatted_timestamp, number, min_distance, mean_distance, max_distance, bits, bytes_n, width, height, stride]
        labels.extend(["Bit per pixel", "Byte per pixel", "Larghezza", "Altezza", "Stride in byte"])
    elif frame_type in ["accel", "gyro"]:
        motion_data = frame.as_motion_frame().get_motion_data()
        orientation = np.arctan2(motion_data.x, np.sqrt(motion_data.y ** 2 + motion_data.z ** 2))
        magnitude = np.sqrt(motion_data.x ** 2 + motion_data.y ** 2 + motion_data.z ** 2)
        data_list = [formatted_timestamp, number, min_distance, mean_distance, max_distance, motion_data.x, motion_data.y, motion_data.z, orientation, magnitude]
        labels.extend(["X", "Y", "Z", "Orientamento", "Magnitudine"])
    return data_list, labels

# Funzione per ottenere il frame di un determinato tipo
def get_frame_by_type(frames, frame_type):
    if frame_type == "depth":
        return frames.get_depth_frame()
    elif frame_type == "color":
        return frames.get_color_frame()
    else:
        return frames.first_or_default(getattr(rs.stream, frame_type))

# Funzione per chiedere all'utente se vuole scegliere la durata della registrazione
def get_valid_choose(arg1, arg2):
    print()
    while True:
        choose = input("Premere 's' per decidere autonomamente la durata della registrazione.\n"
                       "Premere 'n' per registrare fino a quando non si effettua l'interruzione manuale: ")
        if choose.lower() == 's':
            arg1 = get_valid_recording_duration()
            record_data_with_duration(arg1, arg2)
            break
        elif choose.lower() == 'n':
            record_data_until_interrupt(arg2)
            break
        else:
            print("Errore! Scelta non valida!")

# Funzione per chiedere all'utente un input valido per il nome del file
def get_valid_filename():
    while True:
        filename = input("Scegliere il nome del file: ").capitalize()
        csv_path = os.path.join(os.getcwd(), "Realsense CSV", filename, f"{filename} depth data.csv")
        if filename.isalnum() and filename[0].isalpha():
            if not os.path.isfile(csv_path):
                return filename
            else:
                print("Errore! Un file con questo nome esiste già!")
        else:
            print("Errore! Il file deve avere come iniziale una lettera!")

# Funzione per chiedere all'utente un input valido per la durata della registrazione
def get_valid_recording_duration():
    print()
    while True:
        duration = input("Inserire la durata della registrazione in secondi: ")
        if duration.isdigit() and int(duration) > 0:
            return int(duration)
        else:
            print("Errore! Durata non valida!")

# Funzione per chiedere all'utente un input valido per il numero di serie
def get_valid_serial_number():
    while True:
        serial_number = input("Inserire il numero di serie del dispositivo: ")
        if serial_number.isdigit() and len(serial_number) == 12:
            return serial_number
        else:
            print("Errore! Numero di serie non valido!")

# Funzione per inizializzare il dispositivo RealSense e avviare la pipeline
def initialization():
    config = rs.config()
    # Abilita i flussi di dati per profondità, colore, accelerometro e giroscopio
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.accel)
    config.enable_stream(rs.stream.gyro)
    pipeline = rs.pipeline()
    # Avvia la pipeline
    pipeline.start(config)
    return pipeline

# Funzione che verifica se il dispositivo è collegato
def is_device_connected(serial_number):
    context = rs.context()
    devices = context.query_devices()
    return any(device.get_info(rs.camera_info.serial_number) == serial_number for device in devices)

# Funzione per ricevere gli argomenti passati da linea di comando
def receiving_arguments():
    # Lista di argomenti inizializzata con valori di default
    args_list = [-1, -1, -1]
    if len(sys.argv) > 1:
        # Itera attraverso gli argomenti passati
        for i, arg in enumerate(sys.argv[1:4]):
            if arg.isdigit() and len(arg) == 12:
                args_list[0] = arg
            elif arg.isdigit() and int(arg) > 0:
                args_list[1] = int(arg)
            elif arg.isalnum() and arg[0].isalpha:
                args_list[2] = arg
    return args_list

# Funzione per registrare i dati fino a interruzione manuale
def record_data_until_interrupt(filename):
    pipeline = initialization()
    start_time = time.time()
    print("\nDa questo momento, comparirà un punto rosso nella telecamera centrale.\n"
          "Questo significa che la registrazione è iniziata...\n"
          "Premere contemporaneamente 'ctrl' e 'c' per terminare la registrazione.\n"
          "Poi controllare che il punto rosso sia scomparso dalla telecamera centrale.")
    try:
        while True:
            capture_and_save_data(pipeline, filename)
    except KeyboardInterrupt:
        elapsed_time = time.time() - start_time
        print(f"\nRegistrazione interrotta!\n"
              f"La durata della registrazione è di {int(elapsed_time)} secondi.")
    finally:
        stop_pipeline(pipeline)

# Funzione per registrare i dati per una durata specifica
def record_data_with_duration(duration, filename):
    pipeline = initialization()
    start_time = time.time()
    print(f"\nDa questo momento, comparirà un punto rosso nella telecamera centrale.\n"
          f"Questo significa che la registrazione è iniziata...\n"
          f"Dopo {duration} secondi, il punto rosso scomparirà dalla telecamera centrale.\n"
          f"Ciò indica che la registrazione è terminata.")
    while time.time() - start_time < duration:
        capture_and_save_data(pipeline, filename)
    elapsed_time = time.time() - start_time
    print(f"\nRegistrazione interrotta!\n"
          f"La durata della registrazione è di {int(elapsed_time)} secondi.")
    stop_pipeline(pipeline)

# Funzione per salvare i dati in un file CSV
def save_to_csv(filename, data, labels=None):
    # Controlla se il file esiste già
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        if labels and not file_exists:
            # Scrive le etichette se il file non esiste
            writer.writerow(labels)
        # Scrive i dati
        writer.writerow(data)

# Funzione per fermare la pipeline
def stop_pipeline(pipeline):
    pipeline.stop()

# Funzione principale
def main():
    print()
    # Riceve gli argomenti dalla linea di comando
    args = receiving_arguments()
    if args[0] == -1:
        print("Numero di serie non rilevato.")
        # Richiede il numero di serie all'utente
        args[0] = get_valid_serial_number()

    if not is_device_connected(args[0]):
        print("Intel RealSense D435i non è collegato al PC.")
        sys.exit(1)
    else:
        print("Intel RealSense D435i è collegato al PC.")

    if args[2] == -1:
        print("\nNome del file non rilevato.")
        # Richiede il nome del file all'utente
        args[2] = get_valid_filename()
    elif os.path.isfile(os.path.join(os.getcwd(), "Realsense CSV", args[2], f"{args[2]} depth data.csv")):
        print("\nNome del file già esistente.")
        # Richiede un nuovo nome se il file esiste già
        args[2] = get_valid_filename()

    if args[1] == -1:
        # Chiede all'utente se vuole scegliere la durata
        get_valid_choose(args[1], args[2])
    else:
        # Registra per la durata specificata
        record_data_with_duration(args[1], args[2])

if __name__ == "__main__":
    # Esegue la funzione principale
    main()
