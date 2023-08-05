import json

from trytond.tests.test_tryton import POOL, with_transaction
from test_base import BaseTestCase
from decimal import Decimal


class TestWebsite(BaseTestCase):
    """
    Test case for website.
    """

    @with_transaction()
    def test_0010_sitemap(self):
        """
        Tests the rendering of the sitemap.
        """
        self.setup_defaults()
        app = self.get_app()

        node1, = self.Node.create([{
            'name': 'Node1',
            'type_': 'catalog',
            'slug': 'node1',
        }])

        node2, = self.Node.create([{
            'name': 'Node2',
            'type_': 'catalog',
            'slug': 'node2',
            'display': 'product.template',
        }])

        node3, = self.Node.create([{
            'name': 'Node3',
            'type_': 'catalog',
            'slug': 'node3',
        }])

        node4, = self.Node.create([{
            'name': 'Node4',
            'type_': 'catalog',
            'slug': 'node4',
        }])

        node5, = self.Node.create([{
            'name': 'Node5',
            'type_': 'catalog',
            'slug': 'node5',
        }])

        self.Node.write([node2], {
            'parent': node1
        })

        self.Node.write([node3], {
            'parent': node1,
        })

        self.Node.write([node4], {
            'parent': node3,
        })

        self.Node.write([node5], {
            'parent': node4,
        })

        with app.test_client() as c:
            rv = c.get('/sitemap')
            self.assertEqual(rv.status_code, 200)

            self.assertIn('Node1', rv.data)
            self.assertIn('Node2', rv.data)
            self.assertIn('Node3', rv.data)
            self.assertIn('Node4', rv.data)

            # Beyond depth of 2, will not show.
            self.assertNotIn('Node5', rv.data)

    @with_transaction()
    def test_0020_search_data(self):
        """
        Tests that the auto-complete search URL returns JSON product data.
        """
        self.setup_defaults()
        app = self.get_app()

        with app.test_client() as c:
            self.create_test_products()

            rv = c.get('/search-auto-complete?q=product')
            self.assertEqual(rv.status_code, 200)

            data = json.loads(rv.data)

            self.assertEquals(data['results'], [])

    @with_transaction()
    def test0030_menuitem(self):
        '''
        Test create menuitem for products
        '''
        self.Product = POOL.get('product.product')
        self.Template = POOL.get('product.template')
        app = self.get_app()
        self.setup_defaults()
        uom, = self.Uom.search([], limit=1)

        template, = self.Template.create([{
            'name': 'TestProduct',
            'type': 'goods',
            'default_uom': uom.id,
            'list_price': Decimal('100'),
            'cost_price': Decimal('100'),
        }])
        product, = self.Product.create([{
            'template': template.id,
            'displayed_on_eshop': True,
            'uri': 'test-product',
        }])

        with app.test_request_context('/'):
            rv = product.get_menu_item(max_depth=10)

        self.assertEqual(rv['title'], product.name)
