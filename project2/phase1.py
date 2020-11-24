import pymongo
import json
import sys
import multiprocessing as mp


def vote_func(port: int):
    client = pymongo.MongoClient("localhost", port)
    db = client["291db"]

    collection_list = db.list_collection_names()

    if "Votes" in collection_list:
        vote_collection = db.get_collection("Votes")
        vote_collection.drop()

    vote_collection = db.create_collection("Votes")

    with open("Votes.json") as votes:
        votes_data = json.load(votes)
        votes_data = votes_data["votes"]["row"]

        vote_collection.insert_many(votes_data)
        vote_collection.create_index("Id", unique=True, background=True)


def tag_func(port: int):
    client = pymongo.MongoClient("localhost", port)
    db = client["291db"]

    collection_list = db.list_collection_names()

    if "Posts" in collection_list:
        post_collection = db.get_collection("Posts")
        post_collection.drop()

    if "Tags" in collection_list:
        tag_collection = db.get_collection("Tags")
        tag_collection.drop()

    tag_collection = db.create_collection("Tags")

    with open("Tags.json") as tags:
        tags_data = json.load(tags)
        tags_data = tags_data["tags"]["row"]

        tag_collection.insert_many(tags_data)

        tag_collection.create_index("Id", unique=True, background=True)


def post_func(port: int):
    client = pymongo.MongoClient("localhost", port)
    db = client["291db"]

    collection_list = db.list_collection_names()

    if "Posts" in collection_list:
        post_collection = db.get_collection("Posts")
        post_collection.drop()

    post_collection = db.create_collection("Posts")

    with open("Posts.json") as post_file:
        posts_data = json.load(post_file)
        posts_data = posts_data["posts"]["row"]

        post_collection.insert_many(posts_data)

        post_collection.create_index("Id", unique=True, background=True)
        post_collection.create_index(
            [("Body", pymongo.TEXT), ("Title", pymongo.TEXT), ("Tags", pymongo.TEXT)],
            background=True,
        )


if __name__ == "__main__":
    port = 27017
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    post_thread = mp.Process(target=post_func, args=(port,))
    vote_thread = mp.Process(target=vote_func, args=(port,))
    tag_thread = mp.Process(target=tag_func, args=(port,))

    post_thread.start()
    vote_thread.start()
    tag_thread.start()

    vote_thread.join()
    tag_thread.join()
    post_thread.join()
