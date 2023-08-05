# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import os

from flask.helpers import send_from_directory
from trytond.model import ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from nereid import current_app, route, render_template, request, jsonify
from trytond.pyson import Eval, Not

#: Get the static folder. The static folder also
#: goes into the site packages
STATIC_FOLDER = os.path.join(
    os.path.abspath(
        os.path.dirname(__file__)
    ), 'static'
)


class Company(metaclass=PoolMeta):
    __name__ = "company.company"

    logo = fields.Many2One("nereid.static.file", "Logo", select=True)


class WebShop(ModelSQL):
    "Website"
    __name__ = "nereid.webshop"

    @classmethod
    @route("/static-webshop/<path:filename>", methods=["GET"])
    def send_static_file(self, filename):
        """Function used internally to send static files from the static
        folder to the browser.
        """
        cache_timeout = current_app.get_send_file_max_age(filename)
        return send_from_directory(
            STATIC_FOLDER, filename,
            cache_timeout=cache_timeout
        )


class BannerCategory(metaclass=PoolMeta):
    __name__ = 'nereid.cms.banner.category'

    @staticmethod
    def check_xml_record(records, values):
        return True


class Banner(metaclass=PoolMeta):
    __name__ = 'nereid.cms.banner'

    @staticmethod
    def check_xml_record(records, values):
        return True


class Article(metaclass=PoolMeta):
    __name__ = 'nereid.cms.article'

    @staticmethod
    def check_xml_record(records, values):
        """The webshop module creates a bunch of commonly used articles on
        webshops. Since tryton does not allow records created via XML to be
        edited, this method explicitly allows users to modify the articles
        created by the module.
        """
        return True


class ArticleCategory(metaclass=PoolMeta):
    __name__ = 'nereid.cms.article.category'

    @staticmethod
    def check_xml_record(records, values):
        """The webshop module creates a bunch of commonly used article category on
        webshops. Since tryton does not allow records created via XML to be
        edited, this method explicitly allows users to modify the article
        category created by the module.
        """
        return True


class Website(metaclass=PoolMeta):
    __name__ = 'nereid.website'

    cms_root_menu = fields.Many2One(
        'nereid.cms.menuitem', "CMS root menu", ondelete='RESTRICT',
        select=True,
    )

    show_site_message = fields.Boolean('Show Site Message')
    site_message = fields.Char(
        'Site Message',
        states={
            'readonly': Not(Eval('show_site_message', False)),
            'required': Eval('show_site_message', False)
        },
        depends=['show_site_message']
    )

    copyright_year_range = fields.Char('Copyright Year Range')

    cms_root_footer = fields.Many2One(
        'nereid.cms.menuitem', "CMS root Footer", ondelete='RESTRICT',
        select=True,
    )

    homepage_menu = fields.Many2One(
        'nereid.cms.menuitem', "Homepage Menu", ondelete='RESTRICT',
        select=True,
    )
    default_product_image = fields.Many2One("nereid.static.file",
        'Default product image',
        help='This image will be shown as a placeholder if no other '
        'product image is found')

    @classmethod
    @route('/sitemap', methods=["GET"])
    def render_sitemap(cls):
        """
        Return the sitemap.
        """
        Node = Pool().get('product.tree_node')

        # Search for nodes, sort by sequence.
        nodes = Node.search([
            ('parent', '=', None),
        ], order=[
            ('sequence', 'ASC'),
        ])

        return render_template('sitemap.jinja', nodes=nodes)

    @classmethod
    def auto_complete(cls, phrase):
        """
        Customizable method which returns a list of dictionaries
        according to the search query. The search service used can
        be modified in downstream modules.

        The front-end expects a jsonified list of dictionaries. For example,
        a downstream implementation of this method could return -:
        [
            ...
            {
                "value": "<suggestion string>"
            }, {
                "value": "Nexus 6"
            }
            ...
        ]
        """
        return []

    @classmethod
    @route('/search-auto-complete')
    def search_auto_complete(cls):
        """
        Handler for auto-completing search.
        """
        return jsonify(results=cls.auto_complete(
            request.args.get('q', '')
        ))

    @classmethod
    @route('/search')
    def quick_search(cls):
        """
        Downstream implementation of quick_search().

        TODO:
            * Add article search.
        """
        return super(Website, cls).quick_search()

    @staticmethod
    def default_cms_root_footer():
        """
        Get default record from xml
        """
        ModelData = Pool().get('ir.model.data')

        menu_item_id = ModelData.get_id("nereid_webshop", "cms_root_footer")
        return menu_item_id


class MenuItem(metaclass=PoolMeta):
    __name__ = 'nereid.cms.menuitem'

    @staticmethod
    def check_xml_record(records, values):
        return True

    @classmethod
    def allowed_models(cls):
        res = super(MenuItem, cls).allowed_models()

        if ('product.tree_node', 'Tree Node') not in res:
            res.append(('product.tree_node', 'Tree Node'))
        if ('product.product', 'Product') not in res:
            res.append(('product.product', 'Product'))
        return res
