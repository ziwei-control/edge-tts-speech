#!/usr/bin/env python3
"""
语音交互 Web 服务器（带 API 代理）
解决跨域问题，统一端口访问
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import urllib.parse
import json
import os

class ProxyHandler(SimpleHTTPRequestHandler):
    """带 API 代理的 HTTP 处理器"""
    
    def do_GET(self):
        # API 代理
        if self.path.startswith('/api/'):
            self.proxy_api_request('GET')
        else:
            # 静态文件
            super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self.proxy_api_request('POST')
        else:
            self.send_error(404, "Not Found")
    
    def proxy_api_request(self, method):
        """代理请求到 TTS API"""
        try:
            # 移除 /api 前缀
            api_path = self.path[5:]  # /api/health → /health
            # 确保 URL 正确拼接
            if not api_path.startswith('/'):
                api_path = '/' + api_path
            api_url = f"http://localhost:7086{api_path}"
            
            # 获取请求体（POST）
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else None
            
            # 创建请求
            req = urllib.request.Request(api_url, data=post_data, method=method)
            req.add_header('Content-Type', 'application/json')
            
            # 发送请求
            with urllib.request.urlopen(req, timeout=30) as response:
                result = response.read()
                
                # 返回响应
                self.send_response(response.status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(result)
        
        except Exception as e:
            self.send_error(500, f"Proxy Error: {str(e)}")
    
    def do_OPTIONS(self):
        """CORS 预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def end_headers(self):
        """添加 CORS 头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()


def run_server(port=7091):
    """启动 Web 服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ProxyHandler)
    
    print("=" * 60)
    print("🌐 语音交互 Web 服务器（带 API 代理）")
    print("=" * 60)
    print(f"📡 服务地址：http://localhost:{port}")
    print(f"📄 HTML 页面：http://localhost:{port}/voice_chat.html")
    print(f"🔌 API 代理：http://localhost:{port}/api/*")
    print("=" * 60)
    print(f"\n✅ 页面访问：http://localhost:{port}/voice_chat.html")
    print(f"\n💡 提示：API 请求会自动代理到 7086 端口")
    print("=" * 60)
    
    httpd.serve_forever()


if __name__ == '__main__':
    run_server(7091)
