# Models/Assento.py
class Assento:
    def __init__(self, id, onibus_id, localizacao, disponibilidade=True):
        self._id = id
        self._onibus_id = onibus_id
        self._localizacao = localizacao
        self._disponibilidade = disponibilidade

    # Getters
    def get_id(self):
        return self._id

    def get_onibus_id(self):
        return self._onibus_id

    def get_localizacao(self):
        return self._localizacao

    def get_disponibilidade(self):
        return self._disponibilidade

    # Setters
    def set_onibus_id(self, onibus_id):
        self._onibus_id = onibus_id

    def set_localizacao(self, localizacao):
        self._localizacao = localizacao

    def set_disponibilidade(self, disponibilidade):
        self._disponibilidade = disponibilidade