import unittest

from database import Database


class TestUser(unittest.TestCase):
    db = None

    @classmethod
    def setUpClass(cls):
        cls.db = Database(":memory:")

        add_user = "INSERT INTO users (uid, name, pwd, city, crdate) VALUES(?, ?, ?, ?, ?);"
        add_privilege = "INSERT INTO privileged (uid) VALUES(?);"

        cls.db.cursor.execute(add_user, ('n30phyte', 'Mike', '1234', 'Jakarta', '2020-10-29'))
        cls.db.cursor.execute(add_user, ('shadow', 'Cynthia', '12345', 'Edmonton', '2020-09-29'))
        cls.db.cursor.execute(add_user, ('ducklin', 'Azeez', 'abcdef', 'Edmonton', '2019-05-16'))
        cls.db.cursor.execute(add_privilege, ('n30phyte',))

        cls.db.connection.commit()

    def testLoginSuccess(self):
        mike = self.db.login('n30phyte', '1234')
        cynthia = self.db.login('shadow', '12345')
        azeez = self.db.login('ducklin', 'abcdef')

        # Test for success logging in
        self.assertTrue(mike[0])
        self.assertTrue(cynthia[0])
        self.assertTrue(azeez[0])

        # Make sure the correct users returned
        self.assertEqual(mike[1].name, "Mike")
        self.assertEqual(cynthia[1].name, "Cynthia")
        self.assertEqual(azeez[1].name, "Azeez")

    def testPrivilege(self):
        mike = self.db.login('n30phyte', '1234')
        cynthia = self.db.login('shadow', '12345')
        azeez = self.db.login('ducklin', 'abcdef')

        # Verify privilege
        self.assertTrue(mike[1].privileged)
        self.assertFalse(cynthia[1].privileged)
        self.assertFalse(azeez[1].privileged)

    def testLoginFail(self):
        mike = self.db.login('n30phyte', '12345')
        cynthia = self.db.login('shadow', '1234')
        azeez = self.db.login('ducklin', 'abc')
        armi = self.db.login('armiantos', 'uwu')

        # Test for failure logging in
        self.assertFalse(mike[0])
        self.assertFalse(cynthia[0])
        self.assertFalse(azeez[0])
        self.assertFalse(armi[0])

    def testRegisterSuccess(self):
        armi = self.db.register("armiantos", "uwu", "Armianto", "Bali")

        # Test for success registering
        self.assertTrue(armi[0])

        # Make sure the correct users returned
        self.assertEqual(armi[1].name, "Armianto")

    def testRegisterFail(self):
        mike = self.db.register('n30phyte', 'Mike', '1234', 'Jakarta')

        # Test for failure registering
        self.assertFalse(mike[0])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
