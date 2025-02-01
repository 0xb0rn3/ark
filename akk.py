from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load cybersecurity content from JSON file
def load_content():
    content_path = Path(__file__).parent / 'cyber_content.json'
    with open(content_path, 'r') as f:
        return json.load(f)

# Initialize content database
cyber_content = {
    'getting-started': {
        'foundations': {
            'title': 'Core Foundations',
            'content': '''
            Network Fundamentals:
            - TCP/IP Protocol Suite
            - OSI Model
            - Common Protocols (HTTP, DNS, FTP)
            
            Linux Skills:
            - Basic Command Line
            - File System Navigation
            - User Management
            
            Programming Basics:
            - Python Fundamentals
            - Script Writing
            - Automation
            ''',
            'resources': [
                {'name': 'CompTIA Network+', 'url': 'https://www.comptia.org/certifications/network'},
                {'name': 'Linux Essentials', 'url': 'https://www.lpi.org/our-certifications/linux-essentials-overview'},
                {'name': 'Python for Cybersecurity', 'url': 'https://www.coursera.org/learn/python-for-cybersecurity'}
            ]
        },
        # Add more content categories here
    }
}

@app.route('/api/cyber-info/<section>/<topic>', methods=['GET'])
def get_cyber_info(section, topic):
    try:
        content = cyber_content[section][topic]
        return jsonify({
            'status': 'success',
            'data': content
        })
    except KeyError:
        return jsonify({
            'status': 'error',
            'message': 'Content not found'
        }), 404

@app.route('/api/cyber-info/search', methods=['GET'])
def search_content():
    query = request.args.get('q', '').lower()
    results = []
    
    for section, topics in cyber_content.items():
        for topic, content in topics.items():
            if query in content['title'].lower() or query in content['content'].lower():
                results.append({
                    'section': section,
                    'topic': topic,
                    'title': content['title'],
                    'preview': content['content'][:200] + '...'
                })
    
    return jsonify({
        'status': 'success',
        'results': results
    })

if __name__ == '__main__':
    app.run(debug=True)
