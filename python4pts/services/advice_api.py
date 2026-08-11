import requests

ADVICE_URL = "https://api.adviceslip.com/advice"

_FRASE_DEMO = "Um passo de cada vez: conclua uma tarefa hoje e comemore o progresso."

class AdviceApi:

    def __init__(self, url=ADVICE_URL, timeout=5):
        self.url = url
        self.timeout = timeout

    def frase_do_dia(self):
        try:
            resposta = requests.get(self.url, timeout=self.timeout)
            resposta.raise_for_status()
            dados = resposta.json()
            frase = dados.get("slip", {}).get("advice")
            if frase:
                return frase, False
        except (requests.RequestException, ValueError):
            pass

        return _FRASE_DEMO, True
