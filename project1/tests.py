import unittest

from database import Database


class TestUser(unittest.TestCase):
    db = None

    @classmethod
    def setUpClass(cls):
        cls.db = Database(":memory:")

        add_user = "INSERT INTO users (uid, name, pwd, city, crdate) VALUES(?, ?, ?, ?, ?);"
        add_privilege = "INSERT INTO privileged (uid) VALUES(?);"

        cls.db.cursor.execute(add_user, ('n30p', 'Mike', '1234', 'Jakarta', '2020-10-29'))
        cls.db.cursor.execute(add_user, ('shad', 'Cynthia', '12345', 'Edmonton', '2020-09-29'))
        cls.db.cursor.execute(add_user, ('duck', 'Azeez', 'abcdef', 'Edmonton', '2019-05-16'))
        cls.db.cursor.execute(add_privilege, ('n30p',))

        cls.db.connection.commit()

    def testLoginSuccess(self):
        mike_low = self.db.login('n30p', '1234')
        mike_caps = self.db.login('N30P', '1234')
        cynthia_low = self.db.login('shad', '12345')
        cynthia_mix = self.db.login('shaD', '12345')
        azeez_low = self.db.login('duck', 'abcdef')
        azeez_mix = self.db.login('dUck', 'abcdef')

        # Test for success logging in
        self.assertTrue(mike_low[0])
        self.assertTrue(mike_caps[0])

        self.assertTrue(cynthia_low[0])
        self.assertTrue(cynthia_mix[0])

        self.assertTrue(azeez_low[0])
        self.assertTrue(azeez_mix[0])

        # Make sure the correct users returned
        self.assertEqual(mike_low[1].name, mike_caps[1].name)
        self.assertEqual(cynthia_low[1].name, cynthia_mix[1].name)
        self.assertEqual(azeez_low[1].name, azeez_mix[1].name)

    def testPrivilege(self):
        mike = self.db.login('n30p', '1234')
        cynthia = self.db.login('shad', '12345')
        azeez = self.db.login('duck', 'abcdef')

        # Verify privilege
        self.assertTrue(mike[1].privileged)
        self.assertFalse(cynthia[1].privileged)
        self.assertFalse(azeez[1].privileged)

    def testLoginFail(self):
        mike = self.db.login('n30phyte', '12345')
        cynthia = self.db.login('shadow', '1234')
        azeez = self.db.login('ducklin', 'ABCDEF')
        armi = self.db.login('armiantos', 'uwu')

        # Test for failure logging in
        self.assertFalse(mike[0])
        self.assertFalse(cynthia[0])
        self.assertFalse(azeez[0])
        self.assertFalse(armi[0])

    def testRegisterSuccess(self):
        armi = self.db.register("armi", "uwu", "Armianto", "Bali")

        # Test for success registering
        self.assertTrue(armi[0])

        # Make sure the correct users returned
        self.assertEqual(armi[1].name, "Armianto")

    def testRegisterFail(self):
        mike = self.db.register('n30phyte', 'Mike', '1234', 'Jakarta')

        # Test for failure registering
        self.assertFalse(mike[0])


class TestPosts(unittest.TestCase):
    db = None

    @classmethod
    def setUpClass(cls):
        cls.db = Database(":memory:")

        add_user = "INSERT INTO users (uid, name, pwd, city, crdate) VALUES(?, ?, ?, ?, ?);"
        cls.db.cursor.execute(add_user, ('n30p', 'Mike', '1234', 'Jakarta', '2020-10-29'))
        cls.db.cursor.execute(add_user, ('shad', 'Cynthia', '12345', 'Edmonton', '2020-09-29'))
        cls.db.cursor.execute(add_user, ('duck', 'Azeez', 'abcdef', 'Edmonton', '2019-05-16'))

        cls.db.connection.commit()

        (_, cls.mike) = cls.db.login('n30p', '1234')
        (_, cls.cynthia) = cls.db.login('shad', '12345')
        (_, cls.azs) = cls.db.login('duck', 'abcdef')

    def testPosts(self):
        question = self.db.new_question("Why did we pick python", "Yeah what title said. Rust is better", self.mike)

        all_posts = self.db.cursor.execute("SELECT * FROM posts;").fetchall()
        questions = self.db.cursor.execute("SELECT * FROM questions;").fetchall()

        self.assertEqual(len(questions), 1)
        self.assertEqual(len(all_posts), len(questions))

        self.db.new_answer("Why not?", "rust is hard", self.cynthia, question)
        self.db.new_answer("Oh yeah..", "Rust would've been much cooler", self.azs, question)

        good_ans = self.db.new_answer("I've never used rust either", "Learning curve is very steep", self.cynthia,
                                      question)

        answers = self.db.cursor.execute("SELECT * FROM answers;").fetchall()

        self.assertEqual(len(answers), 3)

        # Only one vote should get counted
        self.db.vote_post(good_ans, self.mike)
        self.db.vote_post(good_ans, self.mike)

        self.db.vote_post(good_ans, self.azs)

        votes = self.db.cursor.execute("SELECT * FROM votes;").fetchall()

        self.assertEqual(len(votes), 2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
