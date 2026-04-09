#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import json

class ProxyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/health':
            self.proxy_to_tts('/health')
        elif self.path.startswith('/api/audio/'):
            # 音频文件代理
            filename = self.path.split('/api/audio/')[-1]
            self.send_audio(filename)
        else:
            super().do_GET()
    
    def proxy_to_tts(self, path):
        try:
            with urllib.request.urlopen(f'http://localhost:7086{path}', timeout=10) as resp:
                data = resp.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
        except Exception as e:
            self.send_json({'error': str(e)}, 500)
    
    def send_audio(self, filename):
        try:
            filepath = f'output/api/{filename}'
            with open(filepath, 'rb') as f:
                data = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'audio/mpeg')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
        except Exception as e:
            self.send_json({'error': str(e)}, 404)
    
    def do_POST(self):
        if self.path == '/api/speak':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                req = urllib.request.Request('http://localhost:7086/speak', 
                                            data=post_data,
                                            headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = resp.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                self.send_json({'error': str(e)}, 500)
        else:
            self.send_error(404, "Not Found")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    print("🌐 Web 服务器启动（端口 7091，带 API 代理）")
    HTTPServer(('0.0.0.0', 7091), ProxyHandler).serve_forever()
