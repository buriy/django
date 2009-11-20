from django.test import TestCase


class AdminFilters(TestCase):
    fixtures = ['admin-filter-user.json', 'admin-filter-data.json']
    admin_url = '/test_admin/admin'

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def tearDown(self):
        self.client.logout()

    def test_filters_are_enabled(self):
        """
        log superuser in and go to filtered page
        """
        response = self.client.get('%s/admin_filters/filterable/' % self.admin_url, {'sites__domain': 'example.com'})

        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual('2 filterables' in response.content, True)

