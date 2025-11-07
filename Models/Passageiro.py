# Models/Passageiro.py
class Passageiro:
    def __init__(self, id, numero, assento_id, carteirinha, nome):
        self._id = id
        self._numero = numero
        self._assento_id = assento_id
        self._carteirinha = carteirinha
        self._nome = nome

    # Getters
    def get_id(self):
        return self._id

    def get_numero(self):
        return self._numero

    def get_assento_id(self):
        return self._assento_id

    def get_carteirinha(self):
        return self._carteirinha

    def get_nome(self):
        return self._nome

    # Setters
    def set_numero(self, numero):
        self._numero = numero

    def set_assento_id(self, assento_id):
        self._assento_id = assento_id

    def set_carteirinha(self, carteirinha):
        self._carteirinha = carteirinha

    def set_nome(self, nome):
        self._nome = nome