class AuthService:

    def __init__(self):
        self._token = "kks6sr4X328rGcfoY7W82JdGvFTQViqLt0PbASDlA"

    def validateToken(self, token):
        return token == self._token