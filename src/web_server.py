import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from flask import Flask, request, jsonify
from flask_cors import CORS
from src.controllers.tiktok_posts_scrapper import fetch_tiktok_posts_controller, fetch_comments_for_posts_controller, assign_relevance_scores_and_filter_fasion_posts
from src.controllers.process_fasion_instagram_data import process_fasion_instagram_data

from src.services.mongodb_service import Mongodb_service
from src.configs.mongodb_config import scraped_posts_collection, scraped_posts_with_comments_collection, fasion_posts_collection

from src.database.models.post import Post

app = Flask(__name__)
CORS(app)

@app.route('/')
def health_check():
    return jsonify({"success": True}), 200

@app.route('/scrape_tiktok_posts')
def scrape_tiktok_posts():
    try:
        count = int(request.args.get('posts_to_scrape', 30))
        cursor = int(request.args.get('cursor', 0))

        posts = []
        posts = fetch_tiktok_posts_controller(count, cursor)

        for post in posts:
            post["date_collected"] = str(post["date_collected"])
            post["_id"] = str(post["_id"])
        return jsonify({"success": True, "posts": posts}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/fetch_comments_for_scrapped_posts')
async def fetch_comments_for_scrapped_posts():
    try:
        posts = await fetch_comments_for_posts_controller()

        for post in posts:
            post["date_collected"] = str(post["date_collected"])
            post["_id"] = str(post["_id"])
        return jsonify({"success": True, "posts_with_comments": posts}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/filter_fasion_posts_with_relevance_scores')
def filter_fasion_posts_with_relevance_scores():
    try:
        posts = assign_relevance_scores_and_filter_fasion_posts()

        for post in posts:
            post["date_collected"] = str(post["date_collected"])
            post["_id"] = str(post["_id"])
        return jsonify({"success": True, "posts": posts}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/process_instagram_post_data')
def process_instagram_post_data():
    try:
        num_topics = int(request.args.get('num_topics', 10))
        words_per_topic = int(request.args.get('words_per_topic', 20))
        
        posts = process_fasion_instagram_data(num_topics, words_per_topic)

        return jsonify({"success": True, "posts": posts}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/get_scraped_fasion_posts')
def get_scraped_fasion_posts():
    try:
        mongodb_service_source = Mongodb_service(fasion_posts_collection)
        post_objs_mongo = mongodb_service_source.find()
        
        post_objs = []
        for post_obj_mongo in post_objs_mongo:
            post_obj_mongo["date_collected"] = str(post_obj_mongo["date_collected"])
            post_obj_mongo["_id"] = str(post_obj_mongo["_id"])
            post_objs.append(post_obj_mongo)

        return jsonify({"success": True, "scraped_fasion_posts": post_objs}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/get_scraped_posts')
def get_scraped_posts():
    try:
        mongodb_service_source = Mongodb_service(scraped_posts_collection)
        post_objs_mongo = mongodb_service_source.find()
        
        post_objs = []
        for post_obj_mongo in post_objs_mongo:
            post_obj_mongo["date_collected"] = str(post_obj_mongo["date_collected"])
            post_obj_mongo["_id"] = str(post_obj_mongo["_id"])
            post_objs.append(post_obj_mongo)

        return jsonify({"success": True, "scraped_posts": post_objs}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/get_scraped_posts_with_comments')
def get_scraped_posts_with_comments():
    try:
        
        mongodb_service_source = Mongodb_service(scraped_posts_with_comments_collection)
        post_objs_mongo = mongodb_service_source.find()
        
        post_objs = []
        for post_obj_mongo in post_objs_mongo:
            post_obj_mongo["date_collected"] = str(post_obj_mongo["date_collected"])
            post_obj_mongo["_id"] = str(post_obj_mongo["_id"])
            post_objs.append(post_obj_mongo)

        return jsonify({"success": True, "scraped_posts_with_comments": post_objs}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8000")
