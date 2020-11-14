from datetime import datetime
import random
from typing import List

import pymongo


def date_today() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]


def tag_string(tags: List[str]) -> str:
    output = ""
    for tag in tags:
        output += "<{}> ".format(tag)

    output.strip()

    return output


class Database:
    post_collection = None
    tag_collection = None
    vote_collection = None

    used_post_ids = set()
    used_tag_ids = set()

    def __init__(self, port):
        client = pymongo.MongoClient('localhost', port)
        database = client['291db']

        self.post_collection = database['Posts']
        self.tag_collection = database['Tags']
        self.vote_collection = database['Votes']

    def get_report(self, user: str):
        questions = self.post_collection.find({
            "OwnerUserId": {"$eq": user},
            "PostTypeId": {"$eq": "2"}
        })
        num_questions = len(list(questions))
        question_votes = []
        for q in questions:
            # find number of votes and add to a list
            question_votes.append(len(self.vote_collection.find({
                'PostId': q['Id']
            })))
            pass
        avg_q_votes = sum(question_votes) / len(question_votes)

        answers = self.post_collection.find({
            "OwnerUserId": {"$eq": user},
            "PostTypeId": {"$eq": "2"}
        }).count()
        num_answers = len(answers)
        answer_votes = []
        for a in answers:
            answer_votes.append(len(self.vote_collection.find({
                'PostId': a['Id']
            })))
        avg_a_votes = sum(answer_votes) / len(answer_votes)

        return {
            'num_questions': num_questions,
            'avg_q_votes': avg_q_votes,
            'num_answers': num_answers,
            'avg_a_votes': avg_a_votes
        }

    def new_question(self, user: str, title: str, body: str, tags: List[str]) -> dict:

        self.insert_tags(tags)

        found_id = False
        post_id = 0

        while not found_id:
            post_id = int(random.randint(1, 999999))
            if self.post_collection.find_one({'Id': str(post_id)}) is None:
                found_id = True

        question = {'Id': str(post_id),
                    'OwnerUserId': user,
                    'Title': title,
                    'Body': body,
                    'Tags': tag_string(tags),
                    'CreationDate': date_today(),
                    'PostTypeId': 1,
                    'Score': 0,
                    'ViewCount': 0,
                    'AnswerCount': 0,
                    'CommentCount': 0,
                    'FavouriteCount': 0,
                    'ContentLicense': 'CC BY-SA 2.5'}

        return question

    def search_question(self, keywords: List[str]):
        results = []

        for keyword in keywords:
            result = self.post_collection.find({'$and': [{'$or': [
                {'Body': keyword},
                {'Title': keyword},
                {'Tags': '<' + keyword + '>'}
            ]}, {'PostTypeId': 1}]})

            results.extend(list(result))

        return results

    def visit_question(self, question_id: str):
        # update value in collection
        self.post_collection.update_one({
            'Id': question_id
        }, {
            '$inc': {
                'ViewCount': 1
            }
        })

    def answer_question(self, user: str, question_id: str, body: str):

        found_id = False
        post_id = 0

        while not found_id:
            post_id = int(random.randint(1,999999))
            if self.post_collection.find_one({'Id': str(post_id)}) is None:
                found_id = True

        answer = {'Id': str(post_id),
                  'OwnerUserId': user,
                  'Body': body,
                  'CreationDate': date_today(),
                  'PostTypeId': 2,
                  'Score': 0,
                  'CommentCount': 0,
                  'ContentLicense': 'CC BY-SA 2.5',
                  'ParentId': question_id}

        return answer

    def get_answers(self, question_id: str):
        question_post = self.post_collection.find_one({'$and': [{'Id': question_id},
                                                                {'PostTypeId': 1}]})

        accepted_answer_id = question_post['AcceptedAnswerId']
        accepted_answer = self.post_collection.find_one({'Id': accepted_answer_id})

        answers = self.post_collection.find({'$and': [{'ParentId': question_id},
                                                      {'PostTypeId': 2}]})

        output = list(answers)
        output.insert(0, accepted_answer)

        return output

    def insert_tags(self, tags: List[str]):

        for tag in tags:
            if self.vote_collection.find_one({'TagName': tag}) is None:
                found_id = False
                vote_id = 0

                while not found_id:
                    vote_id = int(random.randint(1, 999999))
                    if self.vote_collection.find_one({'Id': str(vote_id)}) is None:
                        found_id = True

                self.tag_collection.insert_one({'Id': str(vote_id),
                                                'TagName': tag})
