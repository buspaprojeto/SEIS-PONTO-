# Models/Reserva.py
class Reserva:
    def __init__(self, id, passageiro_id, assento_id, data_viagem, status=False):
        self._id = id
        self._passageiro_id = passageiro_id
        self._assento_id = assento_id
        self._data_viagem = data_viagem
        self._status = status

    # Getters
    def get_id(self):
        return self._id

    def get_passageiro_id(self):
        return self._passageiro_id

    def get_assento_id(self):
        return self._assento_id

    def get_data_viagem(self):
        return self._data_viagem

    def get_status(self):
        return self._status

    # Setters
    def set_status(self, status):
        self._status = status
        
# Crie modelos simples (Classes com Getters e Setters) para Assento e Passageiro também.