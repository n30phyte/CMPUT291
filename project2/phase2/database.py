from datetime import datetime
import random
from typing import List

import pymongo


def date_today() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]


def tag_string(tags: List[str]) -> str:
    output = ""
    for tag in tags:
        output += "<{}>".format(tag)

    return output


def deduplicate_posts(posts: List[dict]) -> List[dict]:
    output_list = []

    if len(posts) != 0:
        output_list = [posts[0]]

        for post in posts:
            if post not in output_list:
                output_list.append(post)

    return output_list


class Database:
    post_collection = None
    tag_collection = None
    vote_collection = None

    def __init__(self, port):
        client = pymongo.MongoClient("localhost", port)
        database = client["291db"]

        self.post_collection = database["Posts"]
        self.tag_collection = database["Tags"]
        self.vote_collection = database["Votes"]

    def get_report(self, user: str):
        question_pipeline = [
            {"$match": {"$and": [{"PostTypeId": "1"}, {"OwnerUserId": user}]}},
            {
                "$group": {
                    "_id": "null",
                    "num_questions": {"$sum": 1},
                    "question_score_avg": {"$avg": "$Score"},
                }
            },
        ]

        question_stats = list(self.post_collection.aggregate(question_pipeline))[0]

        answer_pipeline = [
            {"$match": {"$and": [{"PostTypeId": "2"}, {"OwnerUserId": user}]}},
            {
                "$group": {
                    "_id": "null",
                    "num_answers": {"$sum": 1},
                    "answer_score_avg": {"$avg": "$Score"},
                }
            },
        ]

        answer_stats = list(self.post_collection.aggregate(answer_pipeline))[0]

        total_votes = self.vote_collection.count_documents({"UserId": user})

        return {
            "num_questions": question_stats["num_questions"],
            "avg_q_votes": question_stats["question_score_avg"],
            "num_answers": answer_stats["num_answers"],
            "avg_a_votes": answer_stats["answer_score_avg"],
            "total_votes": total_votes,
        }

    def new_post(self, user: str, data: dict) -> dict:
        found_id = False
        post_id = 0

        while not found_id:
            post_id = str(random.randint(1, 999999))
            if self.post_collection.find_one({"Id": post_id}) is None:
                found_id = True

        data["OwnerUserId"] = user
        data["Id"] = post_id
        data["CreationDate"] = date_today()
        data["Score"] = 0
        data["CommentCount"] = 0
        data["ContentLicense"] = "CC BY-SA 2.5"

        self.post_collection.insert_one(data)
        return data

    def new_question(self, user: str, title: str, body: str, tags: List[str]) -> dict:

        self.insert_tags(tags)

        question = {
            "Title": title,
            "Body": body,
            "Tags": tag_string(tags),
            "PostTypeId": str(1),
            "ViewCount": 0,
            "AnswerCount": 0,
            "FavoriteCount": 0,
        }

        return self.new_post(user, question)

    def answer_question(self, user: str, question_id: str, body: str):

        answer = {
            "Body": body,
            "PostTypeId": str(2),
            "ParentId": question_id,
        }

        self.post_collection.update_one(
            {"Id": question_id}, {"$inc": {"AnswerCount": 1}}
        )

        return self.new_post(user, answer)

    def search_question(self, keywords):

        results = list(
            self.post_collection.find(
                {
                    "$and": [
                        {"PostTypeId": "1"},
                        {"$text": {"$search": "{}".format(keywords)}},
                    ]
                }
            ).sort("_id")
        )

        return results

    def visit_question(self, question_id: str):
        # update value in collection
        self.post_collection.update_one({"Id": question_id}, {"$inc": {"ViewCount": 1}})

    def get_answers(self, question_id: str):
        question_post = self.post_collection.find_one(
            {"Id": question_id, "PostTypeId": "1"}
        )

        accepted_answer = None
        accepted_answer_id = ""
        if question_post is not None and "AcceptedAnswerId" in question_post:
            accepted_answer_id = question_post["AcceptedAnswerId"]
            accepted_answer = self.post_collection.find_one({"Id": accepted_answer_id})

        answers = self.post_collection.find(
            {
                "$and": [
                    {"Id": {"$ne": accepted_answer_id}},
                    {"ParentId": question_id},
                    {"PostTypeId": "2"},
                ]
            }
        )

        return accepted_answer, list(answers)

    def vote(self, post_id: str, user_id: str) -> bool:
        # if user already voted on post, do not vote and return false
        if user_id and self.vote_collection.find_one(
            {"PostId": post_id, "UserId": user_id}
        ):
            return False

        # find unused id
        found_id = False
        vote_id = 0
        while not found_id:
            vote_id = int(random.randint(1, 999999))
            if self.vote_collection.find_one({"Id": str(vote_id)}) is None:
                found_id = True

        # create new document and insert into collection
        new_vote = {
            "Id": str(vote_id),
            "PostId": post_id,
            "VoteTypeId": "2",
            "UserId": user_id,
            "CreationDate": date_today(),
        }
        self.vote_collection.insert_one(new_vote)

        # if user id is set, increase score field in Posts by 1
        if user_id:
            self.post_collection.update_one({"Id": post_id}, {"$inc": {"Score": 1}})

        return True

    def insert_tags(self, tags: List[str]):

        for tag in tags:

            if self.tag_collection.find_one({"TagName": tag}) is None:
                found_id = False
                tag_id = 0

                while not found_id:
                    tag_id = int(random.randint(1, 999999))
                    if self.tag_collection.find_one({"Id": str(tag_id)}) is None:
                        found_id = True

                self.tag_collection.insert_one(
                    {"Id": str(tag_id), "TagName": tag, "Count": 1}
                )

            else:
                self.tag_collection.update({"TagName": tag}, {"$inc": {"Count": 1}})
