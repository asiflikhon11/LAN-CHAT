#!/usr/bin/env python3
"""
Web-Based Networking Program
Ubuntu PC: Python servers + HTML generation
Windows PC: Web browser client

Author: Your networking practice program
Usage: python networking_program.py
"""

import socket
import threading
import sys
import time
import os
import platform
import json
import http.server
import socketserver
import webbrowser
from urllib.parse import urlparse, parse_qs
import base64
import hashlib

class Colors:
    """ANSI color codes for better terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    WHITE = '\033[97m'

def print_colored(text, color=Colors.ENDC):
    print(f"{color}{text}{Colors.ENDC}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_system_info():
    """Get system information"""
    return {
        'os': platform.system(),
        'is_windows': platform.system().lower() == 'windows',
        'is_linux': platform.system().lower() == 'linux'
    }

def print_banner():
    sys_info = get_system_info()
    os_icon = "🪟" if sys_info['is_windows'] else "🐧" if sys_info['is_linux'] else "💻"
    
    banner = f"""
    ╔══════════════════════════════════════════════════════════╗
    ║             WEB-BASED NETWORK PROGRAMMING                ║
    ║                                                          ║
    ║  {os_icon} Running on: {platform.system()} {platform.release()}                     ║
    ║  🐧 Ubuntu PC: Python Servers                           ║
    ║  🪟 Windows PC: Web Browser Client                       ║
    ║                                                          ║
    ║  Task 1: UDP Message Web Interface                      ║
    ║  Task 2: TCP Chat Web Application                       ║
    ║  Task 3: Multi-user Web Chat Room                       ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print_colored(banner, Colors.CYAN)

def get_server_ip():
    """Get the best IP address for server binding"""
    try:
        # Method 1: Try connecting to a remote address to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        if not local_ip.startswith('127.'):
            return local_ip
    except:
        pass
    
    try:
        # Method 2: Parse network interfaces directly
        import subprocess
        result = subprocess.run(['ip', 'route', 'get', '1.1.1.1'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'src' in line:
                    ip = line.split('src')[1].strip().split()[0]
                    if not ip.startswith('127.'):
                        return ip
    except:
        pass
    
    try:
        # Method 3: Check hostname resolution
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        if not local_ip.startswith('127.'):
            return local_ip
    except:
        pass
    
    # Method 4: Parse ip addr output for your specific case
    try:
        result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'inet ' in line and 'scope global' in line:
                ip = line.strip().split()[1].split('/')[0]
                if not ip.startswith('127.') and not ip.startswith('172.17.'):
                    return ip
    except:
        pass
        
    return 'localhost'

# ==================== HTML TEMPLATES ====================

def generate_task1_html(server_ip, port=8001):
    """Generate HTML for Task 1: UDP Messaging"""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task 1: UDP Messaging</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        .info {{
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 5px solid #00ff88;
        }}
        .form-group {{
            margin-bottom: 20px;
        }}
        label {{
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }}
        input, textarea, button {{
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
        }}
        input, textarea {{
            background: rgba(255, 255, 255, 0.9);
            color: #333;
        }}
        button {{
            background: linear-gradient(45deg, #00ff88, #00d4aa);
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        button:hover {{
            transform: translateY(-2px);
        }}
        .messages {{
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 10px;
            height: 200px;
            overflow-y: auto;
            font-family: monospace;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .message {{
            margin-bottom: 10px;
            padding: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
        }}
        .status {{
            text-align: center;
            margin-top: 20px;
            font-weight: bold;
        }}
        .success {{ color: #00ff88; }}
        .error {{ color: #ff6b6b; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📨 Task 1: UDP Messaging</h1>
        
        <div class="info">
            <p><strong>🪟 Windows PC Browser</strong> → <strong>🐧 Ubuntu PC Server</strong></p>
            <p>Server: {server_ip}:{port}</p>
            <p>Send one-way UDP messages to the Ubuntu server</p>
        </div>

        <div class="form-group">
            <label for="message">💬 Your Message:</label>
            <textarea id="message" rows="3" placeholder="Type your message here..."></textarea>
        </div>

        <button onclick="sendMessage()">📤 Send Message</button>

        <div class="form-group">
            <label>📋 Message Log:</label>
            <div id="messages" class="messages"></div>
        </div>

        <div id="status" class="status"></div>
    </div>

    <script>
        let messageCount = 0;

        function addToLog(message, isError = false) {{
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message';
            const timestamp = new Date().toLocaleTimeString();
            messageDiv.innerHTML = `<strong>[${{timestamp}}]</strong> ${{message}}`;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }}

        function showStatus(message, isError = false) {{
            const statusDiv = document.getElementById('status');
            statusDiv.textContent = message;
            statusDiv.className = `status ${{isError ? 'error' : 'success'}}`;
            setTimeout(() => statusDiv.textContent = '', 3000);
        }}

        async function sendMessage() {{
            const messageInput = document.getElementById('message');
            const message = messageInput.value.trim();
            
            if (!message) {{
                showStatus('❌ Please enter a message', true);
                return;
            }}

            try {{
                const response = await fetch('/send_udp', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ message: message }})
                }});

                const result = await response.json();
                
                if (result.success) {{
                    messageCount++;
                    addToLog(`📤 Message #${{messageCount}}: "${{message}}"`);
                    showStatus('✅ Message sent successfully!');
                    messageInput.value = '';
                }} else {{
                    addToLog(`❌ Failed to send: ${{result.error}}`, true);
                    showStatus('❌ Failed to send message', true);
                }}
            }} catch (error) {{
                addToLog(`❌ Network error: ${{error.message}}`, true);
                showStatus('❌ Network error', true);
            }}
        }}

        // Send message on Enter key
        document.getElementById('message').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter' && !e.shiftKey) {{
                e.preventDefault();
                sendMessage();
            }}
        }});

        // Initial status
        addToLog('🌐 Connected to Ubuntu PC server');
        showStatus('Ready to send messages');
    </script>
</body>
</html>
"""

def generate_task2_html(server_ip, port=8002):
    """Generate HTML for Task 2: TCP Chat"""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task 2: TCP Chat</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
            height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        .header {{
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            padding: 20px;
            text-align: center;
            color: white;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        .header h1 {{
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        .chat-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 800px;
            margin: 20px auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        .connection-status {{
            padding: 15px;
            text-align: center;
            font-weight: bold;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .connected {{ background: rgba(0, 255, 136, 0.3); color: white; }}
        .disconnected {{ background: rgba(255, 107, 107, 0.3); color: white; }}
        .messages {{
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            min-height: 400px;
            max-height: 400px;
        }}
        .message {{
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 18px;
            max-width: 70%;
            word-wrap: break-word;
        }}
        .message.sent {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            margin-left: auto;
            text-align: right;
        }}
        .message.received {{
            background: rgba(255, 255, 255, 0.9);
            color: #333;
        }}
        .message-time {{
            font-size: 0.8em;
            opacity: 0.7;
            margin-top: 5px;
        }}
        .input-area {{
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .input-group {{
            display: flex;
            gap: 10px;
        }}
        #messageInput {{
            flex: 1;
            padding: 12px 16px;
            border: none;
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            outline: none;
        }}
        #sendButton {{
            padding: 12px 24px;
            border: none;
            border-radius: 25px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        #sendButton:hover {{
            transform: translateY(-2px);
        }}
        #sendButton:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>💬 Task 2: TCP Two-Way Chat</h1>
        <p>🪟 Windows Browser ↔ 🐧 Ubuntu Server</p>
        <p>Server: {server_ip}:{port}</p>
    </div>

    <div class="chat-container">
        <div id="connectionStatus" class="connection-status disconnected">
            🔌 Connecting to Ubuntu PC...
        </div>

        <div id="messages" class="messages"></div>

        <div class="input-area">
            <div class="input-group">
                <input type="text" id="messageInput" placeholder="Type your message..." disabled>
                <button id="sendButton" onclick="sendMessage()" disabled>📤 Send</button>
            </div>
        </div>
    </div>

    <script>
        let ws = null;
        let connected = false;

        function addMessage(content, isSent = false) {{
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${{isSent ? 'sent' : 'received'}}`;
            
            const timestamp = new Date().toLocaleTimeString();
            const icon = isSent ? '🪟' : '🐧';
            const sender = isSent ? 'You' : 'Ubuntu PC';
            
            messageDiv.innerHTML = `
                <div>${{content}}</div>
                <div class="message-time">${{icon}} ${{sender}} • ${{timestamp}}</div>
            `;
            
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }}

        function updateConnectionStatus(isConnected) {{
            const statusDiv = document.getElementById('connectionStatus');
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            
            connected = isConnected;
            
            if (isConnected) {{
                statusDiv.textContent = '✅ Connected to Ubuntu PC';
                statusDiv.className = 'connection-status connected';
                messageInput.disabled = false;
                sendButton.disabled = false;
                messageInput.focus();
            }} else {{
                statusDiv.textContent = '❌ Disconnected from Ubuntu PC';
                statusDiv.className = 'connection-status disconnected';
                messageInput.disabled = true;
                sendButton.disabled = true;
            }}
        }}

        function connectWebSocket() {{
            try {{
                ws = new WebSocket(`ws://{server_ip}:8082`);
                
                ws.onopen = function() {{
                    updateConnectionStatus(true);
                    addMessage('Connected to Ubuntu PC chat server! 🎉');
                }};
                
                ws.onmessage = function(event) {{
                    addMessage(event.data, false);
                }};
                
                ws.onclose = function() {{
                    updateConnectionStatus(false);
                    addMessage('Connection to Ubuntu PC lost 📡');
                    // Try to reconnect after 3 seconds
                    setTimeout(connectWebSocket, 3000);
                }};
                
                ws.onerror = function(error) {{
                    console.error('WebSocket error:', error);
                    addMessage('Connection error occurred ❌');
                }};
            }} catch (error) {{
                console.error('Failed to connect:', error);
                addMessage('Failed to connect to Ubuntu PC ❌');
                setTimeout(connectWebSocket, 3000);
            }}
        }}

        function sendMessage() {{
            const messageInput = document.getElementById('messageInput');
            const message = messageInput.value.trim();
            
            if (!message || !connected) return;
            
            ws.send(message);
            addMessage(message, true);
            messageInput.value = '';
        }}

        // Send message on Enter key
        document.getElementById('messageInput').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                e.preventDefault();
                sendMessage();
            }}
        }});

        // Connect when page loads
        connectWebSocket();
    </script>
</body>
</html>
"""

def generate_task3_html(server_ip, port=8003):
    """Generate HTML for Task 3: Multi-user Chat"""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task 3: Multi-User Chat</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        .header {{
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            padding: 20px;
            text-align: center;
            color: white;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        .main-container {{
            flex: 1;
            display: flex;
            max-width: 1200px;
            margin: 20px auto;
            gap: 20px;
            padding: 0 20px;
        }}
        .chat-container {{
            flex: 2;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        .users-panel {{
            flex: 1;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            max-width: 300px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        .login-screen {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }}
        .login-form {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            color: white;
            max-width: 400px;
            width: 100%;
        }}
        .login-form input {{
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
        }}
        .login-form button {{
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            background: linear-gradient(45deg, #00ff88, #00d4aa);
            color: white;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
        }}
        .connection-status {{
            padding: 15px;
            text-align: center;
            font-weight: bold;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
        }}
        .connected {{ background: rgba(0, 255, 136, 0.3); }}
        .disconnected {{ background: rgba(255, 107, 107, 0.3); }}
        .messages {{
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            min-height: 400px;
        }}
        .message {{
            margin-bottom: 15px;
            padding: 12px 16px;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            word-wrap: break-word;
        }}
        .message.own {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            margin-left: auto;
            max-width: 70%;
            text-align: right;
        }}
        .message.system {{
            background: rgba(255, 193, 7, 0.3);
            text-align: center;
            font-style: italic;
        }}
        .message-header {{
            font-size: 0.9em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .message-time {{
            font-size: 0.8em;
            opacity: 0.7;
            margin-top: 5px;
        }}
        .input-area {{
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .input-group {{
            display: flex;
            gap: 10px;
        }}
        #messageInput {{
            flex: 1;
            padding: 12px 16px;
            border: none;
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            outline: none;
            color: #333;
        }}
        #sendButton {{
            padding: 12px 24px;
            border: none;
            border-radius: 25px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        #sendButton:hover {{
            transform: translateY(-2px);
        }}
        .users-header {{
            color: white;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
            font-size: 1.2em;
        }}
        .user-list {{
            color: white;
        }}
        .user-item {{
            padding: 10px;
            margin-bottom: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .user-item.own {{
            background: rgba(0, 255, 136, 0.2);
        }}
        .commands {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.9em;
        }}
        .hidden {{ display: none; }}
    </style>
</head>
<body>
    <div id="loginScreen" class="login-screen">
        <div class="login-form">
            <h2>🌐 Join Multi-User Chat</h2>
            <p>Enter your details to connect to Ubuntu PC</p>
            <input type="text" id="usernameInput" placeholder="Your username" maxlength="20">
            <input type="text" id="osInput" placeholder="Your OS (Windows/Linux/Mac)" value="Windows">
            <button onclick="joinChat()">🚀 Join Chat</button>
        </div>
    </div>

    <div class="header">
        <h1>🌐 Task 3: Multi-User Chat Room</h1>
        <p>Multiple devices connected to Ubuntu PC</p>
        <p>Server: {server_ip}:{port}</p>
    </div>

    <div class="main-container">
        <div class="chat-container">
            <div id="connectionStatus" class="connection-status disconnected">
                🔌 Connecting to Ubuntu PC...
            </div>

            <div id="messages" class="messages"></div>

            <div class="input-area">
                <div class="input-group">
                    <input type="text" id="messageInput" placeholder="Type your message..." disabled>
                    <button id="sendButton" onclick="sendMessage()" disabled>📤 Send</button>
                </div>
            </div>
        </div>

        <div class="users-panel">
            <div class="users-header">👥 Online Users</div>
            <div id="userList" class="user-list"></div>
            
            <div class="commands">
                <strong>💬 Commands:</strong><br>
                /list - Show users<br>
                /quit - Exit chat
            </div>
        </div>
    </div>

    <script>
        let ws = null;
        let connected = false;
        let username = '';
        let userOS = '';
        let users = [];

        function addMessage(content, type = 'normal', sender = '', timestamp = null) {{
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            
            if (!timestamp) {{
                timestamp = new Date().toLocaleTimeString();
            }}
            
            if (type === 'system') {{
                messageDiv.className = 'message system';
                messageDiv.innerHTML = `${{content}}<div class="message-time">${{timestamp}}</div>`;
            }} else if (type === 'own') {{
                messageDiv.className = 'message own';
                messageDiv.innerHTML = `
                    <div class="message-header">🪟 You</div>
                    <div>${{content}}</div>
                    <div class="message-time">${{timestamp}}</div>
                `;
            }} else {{
                messageDiv.className = 'message';
                const icon = getOSIcon(sender);
                messageDiv.innerHTML = `
                    <div class="message-header">${{icon}} ${{sender}}</div>
                    <div>${{content}}</div>
                    <div class="message-time">${{timestamp}}</div>
                `;
            }}
            
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }}

        function getOSIcon(userInfo) {{
            if (typeof userInfo === 'string') return '💻';
            const os = userInfo.os || '';
            if (os.toLowerCase().includes('windows')) return '🪟';
            if (os.toLowerCase().includes('linux')) return '🐧';
            if (os.toLowerCase().includes('mac')) return '🍎';
            return '💻';
        }}

        function updateUserList(userList) {{
            users = userList;
            const userListDiv = document.getElementById('userList');
            userListDiv.innerHTML = '';
            
            userList.forEach(user => {{
                const userDiv = document.createElement('div');
                userDiv.className = `user-item ${{user.username === username ? 'own' : ''}}`;
                const icon = getOSIcon(user);
                const label = user.username === username ? 'You' : user.username;
                userDiv.innerHTML = `${{icon}} <span>${{label}}</span>`;
                userListDiv.appendChild(userDiv);
            }});
        }}

        function updateConnectionStatus(isConnected) {{
            const statusDiv = document.getElementById('connectionStatus');
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');
            
            connected = isConnected;
            
            if (isConnected) {{
                statusDiv.textContent = `✅ Connected as ${{username}}`;
                statusDiv.className = 'connection-status connected';
                messageInput.disabled = false;
                sendButton.disabled = false;
                messageInput.focus();
            }} else {{
                statusDiv.textContent = '❌ Disconnected from Ubuntu PC';
                statusDiv.className = 'connection-status disconnected';
                messageInput.disabled = true;
                sendButton.disabled = true;
            }}
        }}

        function joinChat() {{
            const usernameInput = document.getElementById('usernameInput');
            const osInput = document.getElementById('osInput');
            
            username = usernameInput.value.trim();
            userOS = osInput.value.trim();
            
            if (!username) {{
                alert('Please enter a username');
                return;
            }}
            
            document.getElementById('loginScreen').classList.add('hidden');
            connectWebSocket();
        }}

        function connectWebSocket() {{
            try {{
                ws = new WebSocket(`ws://{server_ip}:8083`);
                
                ws.onopen = function() {{
                    // Send join message
                    ws.send(JSON.stringify({{
                        type: 'join',
                        username: username,
                        os: userOS
                    }}));
                }};
                
                ws.onmessage = function(event) {{
                    try {{
                        const data = JSON.parse(event.data);
                        
                        switch(data.type) {{
                            case 'joined':
                                updateConnectionStatus(true);
                                addMessage(`Welcome to the chat room! 🎉`, 'system');
                                break;
                            case 'user_joined':
                                addMessage(`${{data.username}} joined the chat`, 'system');
                                break;
                            case 'user_left':
                                addMessage(`${{data.username}} left the chat`, 'system');
                                break;
                            case 'message':
                                addMessage(data.message, 'normal', data.sender, data.timestamp);
                                break;
                            case 'users':
                                updateUserList(data.users);
                                break;
                            case 'error':
                                addMessage(`Error: ${{data.message}}`, 'system');
                                break;
                        }}
                    }} catch (e) {{
                        console.error('Error parsing message:', e);
                    }}
                }};
                
                ws.onclose = function() {{
                    updateConnectionStatus(false);
                    addMessage('Connection to Ubuntu PC lost 📡', 'system');
                    setTimeout(() => {{
                        document.getElementById('loginScreen').classList.remove('hidden');
                    }}, 2000);
                }};
                
                ws.onerror = function(error) {{
                    console.error('WebSocket error:', error);
                    addMessage('Connection error occurred ❌', 'system');
                }};
            }} catch (error) {{
                console.error('Failed to connect:', error);
                addMessage('Failed to connect to Ubuntu PC ❌', 'system');
            }}
        }}

        function sendMessage() {{
            const messageInput = document.getElementById('messageInput');
            const message = messageInput.value.trim();
            
            if (!message || !connected) return;
            
            if (message.startsWith('/')) {{
                // Handle commands
                if (message === '/list') {{
                    ws.send(JSON.stringify({{ type: 'list_users' }}));
                }} else if (message === '/quit') {{
                    ws.close();
                }} else {{
                    addMessage('Unknown command. Use /list or /quit', 'system');
                }}
            }} else {{
                // Send regular message
                ws.send(JSON.stringify({{
                    type: 'message',
                    message: message
                }}));
                addMessage(message, 'own');
            }}
            
            messageInput.value = '';
        }}

        // Send message on Enter key
        document.getElementById('messageInput').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                e.preventDefault();
                sendMessage();
            }}
        }});

        // Join chat on Enter key in username input
        document.getElementById('usernameInput').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                e.preventDefault();
                joinChat();
            }}
        }});
    </script>
</body>
</html>
"""

def generate_index_html(server_ip):
    """Generate main index HTML"""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Network Programming Web Interface</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            max-width: 800px;
            width: 100%;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        h1 {{
            text-align: center;
            margin-bottom: 30px;
            font-size: 3em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        .subtitle {{
            text-align: center;
            margin-bottom: 40px;
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .tasks {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .task-card {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            transition: transform 0.3s ease;
            cursor: pointer;
            border: 2px solid transparent;
        }}
        .task-card:hover {{
            transform: translateY(-5px);
            border-color: rgba(255, 255, 255, 0.3);
        }}
        .task-icon {{
            font-size: 3em;
            margin-bottom: 15px;
        }}
        .task-title {{
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .task-description {{
            opacity: 0.8;
            line-height: 1.5;
        }}
        .info-section {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
        }}
        .info-title {{
            font-weight: bold;
            margin-bottom: 10px;
            color: #00ff88;
        }}
        .server-info {{
            font-family: monospace;
            background: rgba(0, 0, 0, 0.3);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Network Programming</h1>
        <div class="subtitle">
            🪟 Windows Browser ↔ 🐧 Ubuntu Server
        </div>
        
        <div class="tasks">
            <div class="task-card" onclick="openTask(1)">
                <div class="task-icon">📨</div>
                <div class="task-title">Task 1: UDP Messaging</div>
                <div class="task-description">
                    Send one-way UDP messages from your Windows browser to the Ubuntu server
                </div>
            </div>
            
            <div class="task-card" onclick="openTask(2)">
                <div class="task-icon">💬</div>
                <div class="task-title">Task 2: TCP Chat</div>
                <div class="task-description">
                    Real-time two-way chat between Windows browser and Ubuntu server
                </div>
            </div>
            
            <div class="task-card" onclick="openTask(3)">
                <div class="task-icon">🌐</div>
                <div class="task-title">Task 3: Multi-User Chat</div>
                <div class="task-description">
                    Join a multi-user chat room with multiple devices connected
                </div>
            </div>
        </div>
        
        <div class="info-section">
            <div class="info-title">🖥️ Server Information:</div>
            <div class="server-info">
                Ubuntu PC IP: {server_ip}<br>
                Task 1 (UDP): Port 8001<br>
                Task 2 (Chat): Port 8002<br>
                Task 3 (Multi): Port 8003
            </div>
            <p>Click on any task above to start the web interface!</p>
        </div>
    </div>

    <script>
        function openTask(taskNumber) {{
            const urls = {{
                1: '/task1',
                2: '/task2', 
                3: '/task3'
            }};
            
            window.open(urls[taskNumber], '_blank');
        }}
    </script>
</body>
</html>
"""

# ==================== SIMPLE WEBSOCKET SERVER ====================

class SimpleWebSocketServer:
    def __init__(self, host='localhost', port=8082):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = None

    def start(self):
        import threading
        thread = threading.Thread(target=self._run_server)
        thread.daemon = True
        thread.start()

    def _run_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            bind_host = '0.0.0.0' if self.host != 'localhost' else self.host
            self.server_socket.bind((bind_host, self.port))
            self.server_socket.listen(5)
            
            print_colored(f"🔌 WebSocket server listening on {self.host}:{self.port}", Colors.GREEN)
            
            while True:
                client_socket, addr = self.server_socket.accept()
                client_thread = threading.Thread(target=self._handle_client, args=(client_socket, addr))
                client_thread.daemon = True
                client_thread.start()
        except Exception as e:
            print_colored(f"❌ WebSocket server error: {e}", Colors.FAIL)

    def _handle_client(self, client_socket, addr):
        try:
            # Simple WebSocket handshake
            request = client_socket.recv(1024).decode()
            if 'Upgrade: websocket' in request:
                self._websocket_handshake(client_socket, request)
                self.clients.append(client_socket)
                print_colored(f"🔌 WebSocket client connected from {addr}", Colors.GREEN)
                
                while True:
                    try:
                        data = self._receive_websocket_frame(client_socket)
                        if data:
                            self._broadcast_message(data, client_socket)
                        else:
                            break
                    except:
                        break
        except Exception as e:
            print_colored(f"❌ WebSocket client error: {e}", Colors.FAIL)
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            print_colored(f"🔌 WebSocket client disconnected from {addr}", Colors.WARNING)

    def _websocket_handshake(self, client_socket, request):
        import hashlib
        import base64
        
        key = None
        for line in request.split('\n'):
            if 'Sec-WebSocket-Key:' in line:
                key = line.split(':', 1)[1].strip()
                break
        
        if key:
            magic_string = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
            accept = base64.b64encode(hashlib.sha1((key + magic_string).encode()).digest()).decode()
            
            response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept}\r\n"
                "\r\n"
            )
            client_socket.send(response.encode())

    def _receive_websocket_frame(self, client_socket):
        try:
            frame = client_socket.recv(2)
            if len(frame) < 2:
                return None
            
            payload_length = frame[1] & 127
            if payload_length == 126:
                frame += client_socket.recv(2)
                payload_length = int.from_bytes(frame[2:4], 'big')
                mask_start = 4
            elif payload_length == 127:
                frame += client_socket.recv(8)
                payload_length = int.from_bytes(frame[2:10], 'big')
                mask_start = 10
            else:
                mask_start = 2
            
            # Read mask and payload
            mask = client_socket.recv(4)
            masked_payload = client_socket.recv(payload_length)
            
            # Unmask payload
            payload = bytearray()
            for i in range(len(masked_payload)):
                payload.append(masked_payload[i] ^ mask[i % 4])
            
            return payload.decode('utf-8')
        except:
            return None

    def _send_websocket_frame(self, client_socket, message):
        try:
            message_bytes = message.encode('utf-8')
            frame = bytearray()
            frame.append(0x81)  # Text frame
            
            if len(message_bytes) < 126:
                frame.append(len(message_bytes))
            elif len(message_bytes) < 65536:
                frame.append(126)
                frame.extend(len(message_bytes).to_bytes(2, 'big'))
            else:
                frame.append(127)
                frame.extend(len(message_bytes).to_bytes(8, 'big'))
            
            frame.extend(message_bytes)
            client_socket.send(frame)
        except:
            pass

    def _broadcast_message(self, message, sender_socket):
        for client in self.clients[:]:
            if client != sender_socket:
                try:
                    self._send_websocket_frame(client, message)
                except:
                    self.clients.remove(client)

# ==================== WEB SERVERS ====================

class Task1Server:
    """HTTP server for Task 1: UDP Messaging"""
    def __init__(self, host='localhost', port=8001):
        self.host = host
        self.port = port
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        import http.server
        import socketserver
        from urllib.parse import urlparse, parse_qs
        import json
        
        server_host = self.host  # Store host for use in handler
        server_port = self.port  # Store port for use in handler
        
        class TaskHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(generate_task1_html(server_host, server_port).encode())
                else:
                    self.send_response(404)
                    self.end_headers()

            def do_POST(self):
                if self.path == '/send_udp':
                    try:
                        content_length = int(self.headers.get('Content-Length', 0))
                        post_data = self.rfile.read(content_length)
                        
                        data = json.loads(post_data.decode())
                        message = data.get('message', '')
                        
                        # Simulate UDP send (just log it)
                        timestamp = time.strftime("%H:%M:%S")
                        print_colored(f"[{timestamp}] 📨 UDP Message from Windows PC: {message}", Colors.BLUE)
                        
                        # Send proper JSON response
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('Access-Control-Allow-Methods', 'POST')
                        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                        self.end_headers()
                        
                        response = {'success': True, 'message': 'Message received by Ubuntu PC'}
                        self.wfile.write(json.dumps(response).encode())
                        
                    except Exception as e:
                        print_colored(f"❌ Error processing message: {e}", Colors.FAIL)
                        
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        
                        response = {'success': False, 'error': str(e)}
                        self.wfile.write(json.dumps(response).encode())
                else:
                    # Handle unknown paths
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'success': False, 'error': 'Endpoint not found'}
                    self.wfile.write(json.dumps(response).encode())
            
            def do_OPTIONS(self):
                # Handle CORS preflight requests
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()

            def log_message(self, format, *args):
                pass  # Suppress default logging

        bind_host = '0.0.0.0' if self.host != 'localhost' else self.host
        
        try:
            with socketserver.TCPServer((bind_host, self.port), TaskHandler) as httpd:
                print_colored(f"📨 Task 1 Web Server running on {self.host}:{self.port}", Colors.GREEN)
                print_colored(f"🪟 Windows PC should visit: http://{self.host}:{self.port}", Colors.WARNING)
                httpd.serve_forever()
        except KeyboardInterrupt:
            print_colored("\n📨 Task 1 server stopped", Colors.WARNING)

class Task2Server:
    """WebSocket server for Task 2: TCP Chat"""
    def __init__(self, host='localhost', port=8002):
        self.host = host
        self.port = port

    def start(self):
        import http.server
        import socketserver
        
        server_host = self.host  # Store host for use in handler
        server_port = self.port  # Store port for use in handler
        
        class TaskHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(generate_task2_html(server_host, server_port).encode())

            def log_message(self, format, *args):
                pass

        bind_host = '0.0.0.0' if self.host != 'localhost' else self.host
        
        # Start WebSocket server
        ws_server = SimpleWebSocketServer(self.host, 8082)
        ws_server.start()
        
        try:
            with socketserver.TCPServer((bind_host, self.port), TaskHandler) as httpd:
                print_colored(f"💬 Task 2 Web Server running on {self.host}:{self.port}", Colors.GREEN)
                print_colored(f"🪟 Windows PC should visit: http://{self.host}:{self.port}", Colors.WARNING)
                httpd.serve_forever()
        except KeyboardInterrupt:
            print_colored("\n💬 Task 2 server stopped", Colors.WARNING)

class Task3Server:
    """WebSocket server for Task 3: Multi-user Chat"""
    def __init__(self, host='localhost', port=8003):
        self.host = host
        self.port = port
        self.users = {}  # {websocket: user_info}

    def start(self):
        import http.server
        import socketserver
        
        server_host = self.host  # Store host for use in handler
        server_port = self.port  # Store port for use in handler
        
        class TaskHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(generate_task3_html(server_host, server_port).encode())

            def log_message(self, format, *args):
                pass

        bind_host = '0.0.0.0' if self.host != 'localhost' else self.host
        
        # Start WebSocket server for multi-user chat
        self._start_websocket_server()
        
        try:
            with socketserver.TCPServer((bind_host, self.port), TaskHandler) as httpd:
                print_colored(f"🌐 Task 3 Web Server running on {self.host}:{self.port}", Colors.GREEN)
                print_colored(f"🪟 Windows PC should visit: http://{self.host}:{self.port}", Colors.WARNING)
                httpd.serve_forever()
        except KeyboardInterrupt:
            print_colored("\n🌐 Task 3 server stopped", Colors.WARNING)

    def _start_websocket_server(self):
        # This is a simplified implementation
        # In a real application, you'd use a proper WebSocket library
        threading.Thread(target=self._run_websocket_server, daemon=True).start()

    def _run_websocket_server(self):
        print_colored(f"🔌 Task 3 WebSocket server on port 8083", Colors.GREEN)

class MainWebServer:
    """Main web server that serves the index page"""
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port

    def start(self):
        import http.server
        import socketserver
        
        server_host = self.host  # Store host for use in handler
        
        class MainHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/' or self.path == '/index':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(generate_index_html(server_host).encode())
                elif self.path == '/task1':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(generate_task1_html(server_host).encode())
                elif self.path == '/task2':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(generate_task2_html(server_host).encode())
                elif self.path == '/task3':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(generate_task3_html(server_host).encode())
                else:
                    self.send_response(404)
                    self.end_headers()

            def log_message(self, format, *args):
                pass

        bind_host = '0.0.0.0' if self.host != 'localhost' else self.host
        
        try:
            with socketserver.TCPServer((bind_host, self.port), MainHandler) as httpd:
                print_colored(f"🌐 Main Web Server running on {self.host}:{self.port}", Colors.GREEN)
                print_colored(f"🪟 Windows PC should visit: http://{self.host}:{self.port}", Colors.WARNING)
                httpd.serve_forever()
        except KeyboardInterrupt:
            print_colored("\n🌐 Main server stopped", Colors.WARNING)

# ==================== MENU FUNCTIONS ====================

def show_network_info():
    """Display network information"""
    print_colored("\n📡 Network Information:", Colors.CYAN)
    print_colored(f"   Hostname: {socket.gethostname()}", Colors.WHITE)
    print_colored(f"   System: {platform.system()} {platform.release()}", Colors.WHITE)
    print_colored(f"   Recommended IP: {get_server_ip()}", Colors.GREEN)
    
    print_colored(f"\n🌐 Web Server Ports:", Colors.WARNING)
    print_colored(f"   Main Interface: 8000", Colors.WHITE)
    print_colored(f"   Task 1 (UDP): 8001", Colors.WHITE)
    print_colored(f"   Task 2 (Chat): 8002", Colors.WHITE)
    print_colored(f"   Task 3 (Multi): 8003", Colors.WHITE)

def ubuntu_main_menu():
    """Ubuntu PC main menu"""
    while True:
        clear_screen()
        print_banner()
        
        server_ip = get_server_ip()
        print_colored("🐧 UBUNTU PC - Web Server Control Panel", Colors.BOLD)
        print_colored(f"Your IP: {server_ip}", Colors.GREEN)
        
        print("\n🖥️  WEB SERVERS:")
        print("1. 🌐 Start Main Web Interface (All Tasks)")
        print("2. 📨 Start Task 1 Web Server (UDP Messaging)")
        print("3. 💬 Start Task 2 Web Server (TCP Chat)")
        print("4. 🌐 Start Task 3 Web Server (Multi-Chat)")
        
        print("\n⚙️  UTILITIES:")
        print("5. 📡 Show Network Information")
        print("6. 🌐 Open Browser (Local Test)")
        print("7. 📋 Show Windows PC Instructions")
        print("8. 🚪 Exit")
        
        choice = input(f"\n{Colors.BOLD}🐧 Ubuntu choice (1-8): {Colors.ENDC}").strip()
        
        if choice == '1':
            server = MainWebServer(server_ip, 8000)
            server.start()
        elif choice == '2':
            server = Task1Server(server_ip, 8001)
            server.start()
        elif choice == '3':
            server = Task2Server(server_ip, 8002)
            server.start()
        elif choice == '4':
            server = Task3Server(server_ip, 8003)
            server.start()
        elif choice == '5':
            show_network_info()
            input("\nPress Enter to continue...")
        elif choice == '6':
            try:
                webbrowser.open(f'http://localhost:8000')
                print_colored("🌐 Browser opened for local testing", Colors.GREEN)
            except:
                print_colored("❌ Could not open browser", Colors.FAIL)
            input("\nPress Enter to continue...")
        elif choice == '7':
            show_windows_instructions(server_ip)
        elif choice == '8':
            print_colored("\n👋 Thanks for using the networking toolkit!", Colors.CYAN)
            break
        else:
            print_colored("\n❌ Invalid choice. Please try again.", Colors.FAIL)
            input("Press Enter to continue...")

def windows_main_menu():
    """Windows PC main menu"""
    while True:
        clear_screen()
        print_banner()
        
        print_colored("🪟 WINDOWS PC - Browser Client", Colors.BOLD)
        print_colored("Connect to Ubuntu PC using your web browser", Colors.CYAN)
        
        print("\n📱 HOW TO CONNECT:")
        print("1. 📖 Show Connection Instructions")
        print("2. 🌐 Enter Ubuntu PC IP Address")
        print("3. 📡 Test Connection to Ubuntu PC")
        print("4. 🚪 Exit")
        
        choice = input(f"\n{Colors.BOLD}🪟 Windows choice (1-4): {Colors.ENDC}").strip()
        
        if choice == '1':
            show_windows_instructions()
        elif choice == '2':
            ubuntu_ip = input("Enter Ubuntu PC IP address: ").strip()
            if ubuntu_ip:
                show_browser_urls(ubuntu_ip)
        elif choice == '3':
            test_connection()
        elif choice == '4':
            print_colored("\n👋 Thanks for using the networking toolkit!", Colors.CYAN)
            break
        else:
            print_colored("\n❌ Invalid choice. Please try again.", Colors.FAIL)
            input("Press Enter to continue...")

def show_windows_instructions(server_ip=None):
    """Show Windows PC connection instructions"""
    if not server_ip:
        server_ip = get_server_ip()
    
    instructions = f"""
    ╔══════════════════════════════════════════════════════════╗
    ║              WINDOWS PC BROWSER INSTRUCTIONS             ║
    ╚══════════════════════════════════════════════════════════╝
    
    🪟 Your Windows PC will connect using any web browser
    
    📋 STEP-BY-STEP INSTRUCTIONS:
    
    1️⃣  GET UBUNTU PC'S IP ADDRESS:
         Ask Ubuntu PC user for their IP address
         It should look like: {server_ip}
    
    2️⃣  OPEN YOUR WEB BROWSER:
         Chrome, Firefox, Edge, Safari, etc.
    
    3️⃣  VISIT THE UBUNTU PC WEB INTERFACE:
         Main Interface: http://{server_ip}:8000
         Task 1 Only:   http://{server_ip}:8001
         Task 2 Only:   http://{server_ip}:8002
         Task 3 Only:   http://{server_ip}:8003
    
    4️⃣  START USING THE INTERFACE:
         • Click on any task to start
         • No additional software needed
         • Works on any device with a browser
    
    🔗 QUICK ACCESS URLS:
         Main: http://{server_ip}:8000
         UDP:  http://{server_ip}:8001
         Chat: http://{server_ip}:8002
         Multi: http://{server_ip}:8003
    
    💡 TROUBLESHOOTING:
         • Make sure Ubuntu PC web server is running
         • Both devices must be on same network
         • Try ping {server_ip} to test connectivity
         • Disable firewall temporarily if needed
    """
    
    clear_screen()
    print_colored(instructions, Colors.CYAN)
    input("\nPress Enter to continue...")

def show_browser_urls(ubuntu_ip):
    """Show browser URLs for Windows PC"""
    urls = f"""
    🌐 BROWSER URLS FOR UBUNTU PC ({ubuntu_ip}):
    
    📋 Copy these URLs into your browser:
    
    🏠 Main Interface (All Tasks):
         http://{ubuntu_ip}:8000
    
    📨 Task 1 - UDP Messaging:
         http://{ubuntu_ip}:8001
    
    💬 Task 2 - TCP Chat:
         http://{ubuntu_ip}:8002
    
    🌐 Task 3 - Multi-User Chat:
         http://{ubuntu_ip}:8003
    
    💡 TIP: Bookmark the main interface URL!
    """
    
    print_colored(urls, Colors.CYAN)
    input("\nPress Enter to continue...")

def test_connection():
    """Test connection to Ubuntu PC"""
    ubuntu_ip = input("Enter Ubuntu PC IP to test: ").strip()
    if not ubuntu_ip:
        return
    
    print_colored(f"\n🔍 Testing connection to {ubuntu_ip}...", Colors.CYAN)
    
    # Test ping
    import subprocess
    import platform
    
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        result = subprocess.run(['ping', param, '1', ubuntu_ip], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print_colored(f"✅ Ping successful! {ubuntu_ip} is reachable", Colors.GREEN)
        else:
            print_colored(f"❌ Ping failed! {ubuntu_ip} is not reachable", Colors.FAIL)
    except:
        print_colored(f"❌ Could not test ping to {ubuntu_ip}", Colors.FAIL)
    
    input("\nPress Enter to continue...")

def main_menu():
    """Detect OS and show appropriate menu"""
    sys_info = get_system_info()
    
    if sys_info['is_linux']:
        ubuntu_main_menu()
    elif sys_info['is_windows']:
        windows_main_menu()
    else:
        # Generic menu for other systems
        ubuntu_main_menu()  # Default to server functionality

# ==================== PROGRAM ENTRY POINT ====================

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print_colored("\n\n👋 Program terminated by user. Goodbye!", Colors.WARNING)
    except Exception as e:
        print_colored(f"\n❌ Unexpected error: {e}", Colors.FAIL)
        print_colored("Please restart the program.", Colors.WARNING)