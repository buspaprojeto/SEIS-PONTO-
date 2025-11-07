# Models/Onibus.py
class Onibus:
    def __init__(self, id, motorista, id_coordenador):
        self._id = id
        self._motorista = motorista
        self._id_coordenador = id_coordenador

    # Getters
    def get_id(self):
        return self._id

    def get_motorista(self):
        return self._motorista

    def get_id_coordenador(self):
        return self._id_coordenador

    # Setters
    def set_id(self, id):
        self._id = id

    def set_motorista(self, motorista):
        self._motorista = motorista

    def set_id_coordenador(self, id_coordenador):
        self._id_coordenador = id_coordenador