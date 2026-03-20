# filepath: c:\Users\Rafael\OneDrive\Anexos\Área de Trabalho\site\cleitan-os\core\scanner.py
import socket

class NetworkScanner:
    def __init__(self, target):
        self.target = target
        self.open_ports = []

    def scan_ports(self, start_port=1, end_port=1024):
        """Escaneia as portas de um alvo específico."""
        for port in range(start_port, end_port + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)  # Define um tempo limite para a conexão
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    self.open_ports.append(port)

    def get_open_ports(self):
        """Retorna uma lista de portas abertas."""
        return self.open_ports

    def display_results(self):
        """Exibe os resultados da varredura."""
        if self.open_ports:
            print(f"Portas abertas em {self.target}: {', '.join(map(str, self.open_ports))}")
        else:
            print(f"Nenhuma porta aberta encontrada em {self.target}.")