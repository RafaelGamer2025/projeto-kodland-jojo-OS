# filepath: c:\Users\Rafael\OneDrive\Anexos\Área de Trabalho\site\cleitan-os\core\ports.py

import socket

class PortScanner:
    def __init__(self, target):
        self.target = target
        self.open_ports = []

    def scan(self, start_port, end_port):
        """Escaneia as portas de start_port a end_port no alvo especificado."""
        print(f"Escaneando {self.target} de porta {start_port} a {end_port}...")
        for port in range(start_port, end_port + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)  # Define um tempo limite de 1 segundo
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    self.open_ports.append(port)
                    print(f"Porta {port} está aberta.")
                else:
                    print(f"Porta {port} está fechada.")

    def get_open_ports(self):
        """Retorna uma lista de portas abertas encontradas durante o escaneamento."""
        return self.open_ports

# Exemplo de uso:
# if __name__ == "__main__":
#     scanner = PortScanner("127.0.0.1")
#     scanner.scan(1, 1024)
#     print("Portas abertas:", scanner.get_open_ports())