class UsuarioLogado:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UsuarioLogado, cls).__new__(cls)
            cls._instance._usuario_logado = None
            cls._instance._authenticated = False
        return cls._instance

    def get_usuario_logado(self):
        return self._usuario_logado

    def set_usuario_logado(self, usuario):
        self._usuario_logado = usuario
        self._authenticated = True

    def autenticado(self):
        return self._authenticated