import pymongo
import json

# todo: update to connect to port from args
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['291db']

# create collections
db.create_collection("Posts")
posts_collection = db.get_collection("Posts")
db.create_collection("Tags")
tags_collection = db.get_collection("Tags")
db.create_collection("Votes")
votes_collection = db.get_collection("Votes")

# insert file data
with open("Posts.json") as posts:
    posts_data = json.load(posts)
posts_collection.insert_many(posts_data)

with open("Tags.json") as tags:
    tags_data = json.load(tags)
tags_collection.insert_many(tags_data)

with open("Votes.json") as votes:
    votes_data = json.load(votes)
votes_collection.insert_many(votes_data)