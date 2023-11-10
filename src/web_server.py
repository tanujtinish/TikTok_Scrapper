import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from flask import Flask, request, jsonify
from flask_cors import CORS
from src.jobs.tiktok_posts_scrapper import fetch_tiktok_fasion_posts_job

app = Flask(__name__)
CORS(app)

@app.route('/')
def health_check():
    return jsonify({"success": True}), 200

@app.route('/fetch_fasion_posts')
def fetch_fasion_posts():
    try:
        count = int(request.args.get('posts_to_scrape', 30))
        count = int(request.args.get('fasion_posts_needed', -1))
        fetch_comments = bool(request.args.get('fetch_comments', False))
        
        print(count)
        print(fetch_comments)

        posts = []
        posts = fetch_tiktok_fasion_posts_job(count, fetch_comments)

        return jsonify({"success": True, "posts": posts}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8000")
