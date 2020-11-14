import pymongo
import json
import sys

if __name__ == "__main__":
    port = 27017
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    client = pymongo.MongoClient('localhost', port)
    db = client['291db']

    collection_list = db.list_collection_names()

    # Check for existence and delete if exists
    if ("Posts" in collection_list):
        post_collection = db.get_collection("Posts")
        post_collection.drop()

    post_collection = db.create_collection("Posts")

    if ("Tags" in collection_list):
        tag_collection = db.get_collection("Tags")
        tag_collection.drop()

    tag_collection = db.create_collection("Tags")

    if ("Votes" in collection_list):
        vote_collection = db.get_collection("Votes")
        vote_collection.drop()

    vote_collection = db.create_collection("Votes")

    # insert file data
    with open("Posts.json") as post_file:
        posts_data = json.load(post_file)
        posts_data = posts_data["posts"]["row"]

        post_collection.insert_many(posts_data)

    with open("Tags.json") as tags:
        tags_data = json.load(tags)
        tags_data = tags_data["tags"]["row"]

        tag_collection.insert_many(tags_data)

    with open("Votes.json") as votes:
        votes_data = json.load(votes)
        votes_data = votes_data["votes"]["row"]

        vote_collection.insert_many(votes_data)
