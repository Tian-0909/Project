#!/usr/bin/env python3
"""
简单的HTTP服务器启动脚本
用于在本地运行MetaMask演示页面

使用方法:
python3 start_server.py

然后在浏览器中访问: http://localhost:8000
"""

import http.server
import socketserver
import webbrowser
import os
import sys

# 设置端口
PORT = 8000

# 切换到脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 创建支持UTF-8的HTTP服务器
class UTF8Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 为HTML文件设置UTF-8编码
        if self.path.endswith('.html') or self.path.endswith('.htm'):
            self.send_header('Content-Type', 'text/html; charset=utf-8')
        elif self.path.endswith('.css'):
            self.send_header('Content-Type', 'text/css; charset=utf-8')
        elif self.path.endswith('.js'):
            self.send_header('Content-Type', 'application/javascript; charset=utf-8')
        super().end_headers()

Handler = UTF8Handler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("=" * 50)
        print("🚀 MetaMask演示服务器启动成功！")
        print("=" * 50)
        print(f"📍 服务器地址: http://localhost:{PORT}")
        print(f"📁 服务目录: {script_dir}")
        print("📄 主页面: http://localhost:{PORT}/Wallet.html")
        print("=" * 50)
        print("💡 提示:")
        print("1. 确保已安装MetaMask浏览器插件")
        print("2. 在浏览器中访问上述地址")
        print("3. 按 Ctrl+C 停止服务器")
        print("=" * 50)
        
        # 自动打开浏览器
        try:
            webbrowser.open(f'http://localhost:{PORT}/Wallet.html')
            print("🌐 正在自动打开浏览器...")
        except:
            print("⚠️ 无法自动打开浏览器，请手动访问上述地址")
        
        print("\n服务器运行中，按 Ctrl+C 停止...")
        httpd.serve_forever()
        
except KeyboardInterrupt:
    print("\n👋 服务器已停止")
    sys.exit(0)
except OSError as e:
    if e.errno == 48:  # Address already in use
        print(f"❌ 端口 {PORT} 已被占用，请使用其他端口或停止占用该端口的程序")
        # 尝试使用其他端口
        for port in range(8001, 8010):
            try:
                with socketserver.TCPServer(("", port), Handler) as httpd:
                    print(f"✅ 改用端口 {port}")
                    print(f"📄 主页面: http://localhost:{port}/Wallet.html")
                    webbrowser.open(f'http://localhost:{port}/Wallet.html')
                    httpd.serve_forever()
                    break
            except OSError:
                continue
    else:
        print(f"❌ 启动服务器失败: {e}")
        sys.exit(1)
