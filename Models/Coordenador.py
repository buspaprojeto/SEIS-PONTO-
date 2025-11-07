# Models/Coordenador.py
class Coordenador:
    def __init__(self, id, nome, numero):
        self._id = id
        self._nome = nome
        self._numero = numero

    # Getters
    def get_id(self):
        return self._id

    def get_nome(self):
        return self._nome

    def get_numero(self):
        return self._numero

    # Setters
    def set_id(self, id):
        self._id = id

    def set_nome(self, nome):
        self._nome = nome

    def set_numero(self, numero):
        if numero < 0:
            raise ValueError("Número de contato não pode ser negativo")
        self._numero = numero