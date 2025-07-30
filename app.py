from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    url = f"https://google.com/{path}"
    if request.query_string:
        url += '?' + request.query_string.decode()

    headers = {
        "User-Agent": request.headers.get("User-Agent", "Mozilla/5.0")
    }

    try:
        r = requests.get(url, headers=headers, stream=True, timeout=10)
        excluded = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = [(k, v) for k, v in r.raw.headers.items() if k.lower() not in excluded]
        return Response(r.content, r.status_code, response_headers)
    except Exception as e:
        return f"Erro ao acessar YouTube: {str(e)}", 500

if __name__ == '__main__':
    app.run()
