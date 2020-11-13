from datetime import datetime
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

    next_post_id = 0
    next_tag_id = 0

    def __init__(self, port):
        client = pymongo.MongoClient('localhost', port)
        database = client['291db']

        self.post_collection = database['Posts']
        self.tag_collection = database['Tags']
        self.vote_collection = database['Votes']

        latest_post = self.post_collection.find_one(sort=[("Id", pymongo.DESCENDING)])
        self.next_post_id = latest_post['Id'] + 1

        latest_tag = self.tag_collection.find_one(sort=[("Id", pymongo.DESCENDING)])
        self.next_tag_id = latest_tag['Id'] + 1

    def new_question(self, user: int, title: str, body: str, tags: List[str]):

        self.insert_tags(tags)

        question = {'Id': self.next_post_id,
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

        self.next_post_id += 1

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

    def answer_question(self, user: int, question_id: int, body: str):
        answer = {'Id': self.next_post_id,
                  'OwnerUserId': user,
                  'Body': body,
                  'CreationDate': date_today(),
                  'PostTypeId': 2,
                  'Score': 0,
                  'CommentCount': 0,
                  'ContentLicense': 'CC BY-SA 2.5',
                  'ParentId': question_id}
        self.next_post_id += 1

        return answer

    def get_answers(self, question_id: int):
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
            self.tag_collection.insert_one({'Id': self.next_tag_id,
                                            'TagName': tag})
            self.next_tag_id += 1