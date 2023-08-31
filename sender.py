import serial
import keyboard
import time

# Defina a porta serial correta e a velocidade (baud rate) adequada
port = "/dev/ttyACM0"  # Caminho da porta serial correto
baud_rate = 115200

try:
    ser = serial.Serial(port=port, baudrate=baud_rate, timeout=0.1)
    print(f"Conectado à porta serial {port}.")

    print("Pressione 'w' para frente, 'a' para esquerda, 'd' para direita, 's' para trás.")

    while True:
        # Verifique se alguma das teclas está pressionada
        if keyboard.is_pressed("w"):
            ser.write(b'w')  # Use b'w' para enviar o byte correspondente ao caractere 'w'
        elif keyboard.is_pressed("a"):
            ser.write(b'a')
        elif keyboard.is_pressed("d"):
            ser.write(b'd')
        elif keyboard.is_pressed("s"):
            ser.write(b's')
        else:
            ser.write(b'stop')  # Envia um comando para parar o movimento

        time.sleep(0.1)  # Pequeno atraso para evitar leituras repetidas
except KeyboardInterrupt:
    ser.close()
    print("Conexão serial fechada.")
