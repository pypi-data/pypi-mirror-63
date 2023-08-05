from random import randint
from tests.sharepoint_case import SPTestCase
from tests.test_utilities import WebExtensions
from office365.sharepoint.web_creation_information import WebCreationInformation


class TestSharePointWeb(SPTestCase):
    target_web = None

    @classmethod
    def setUpClass(cls):
        super(TestSharePointWeb, cls).setUpClass()

    def test1_can_create_web(self):
        self.client.execute_query()  # force to clear the pending queue
        target_web_name = "workspace_" + str(randint(0, 100000))
        creation_info = WebCreationInformation()
        creation_info.Url = target_web_name
        creation_info.Title = target_web_name
        self.__class__.target_web = self.client.web.webs.add(creation_info)
        self.client.execute_query()

        results = self.client.web.webs.filter("Title eq '{0}'".format(target_web_name))
        self.client.load(results)
        self.client.execute_query()
        self.assertEqual(len(results), 1)
        self.assertIsNotNone(results[0].resourceUrl)

    def test2_if_web_updated(self):
        """Test to update Web resource"""
        web_title_updated = self.__class__.target_web.properties["Title"] + "_updated"
        self.__class__.target_web.set_property("Title", web_title_updated)
        self.__class__.target_web.update()
        self.client.execute_query()

        self.client.load(self.__class__.target_web)
        self.client.execute_query()
        self.assertEqual(web_title_updated, self.__class__.target_web.properties['Title'])

    def test3_if_web_deleted(self):
        """Test to delete Web resource"""
        title = self.__class__.target_web.properties['Title']
        self.__class__.target_web.delete_object()
        self.client.execute_query()

        results = self.client.web.webs.filter("Title eq '{0}'".format(title))
        self.client.load(results)
        self.client.execute_query()
        self.assertEqual(len(results), 0)

    def test4_enum_all_webs(self):
        """Test to enumerate all webs within site"""
        all_webs = WebExtensions.get_all_webs(self.client.web)
        self.client.execute_query()
        self.assertTrue(len(all_webs) > 0)
