import frappe
import json ###Custom
from frappe.utils import cint

from webshop.webshop.product_data_engine.filters import ProductFiltersBuilder

sitemap = 1


def get_context(context, filters = None):
	# Add homepage as parent
	context.body_class = "product-page"
	context.parents = [{"name": frappe._("Home"), "route": "/"}]

	filter_engine = ProductFiltersBuilder()
	context.field_filters = filter_engine.get_field_filters()
	context.attribute_filters = filter_engine.get_attribute_filters()

	context.page_length = (
		cint(frappe.db.get_single_value("Webshop Settings", "products_per_page")) or 20
	)

	context.no_cache = 1



@frappe.whitelist(allow_guest=True)
def get_filters(query_args=None):
	if isinstance(query_args, str):
		query_args = json.loads(query_args)
		frappe.log_error("queryargs",query_args)

	query_args = frappe._dict(query_args)
	frappe.log_error("queryargs",query_args)

	if query_args:
		frappe.log_error("got into",query_args)
		field_filters = query_args.get("field_filters", {})
		frappe.log_error("field filterhgs",field_filters)
		filter_engine = ProductFiltersBuilder(filters = field_filters)  
		filters = filter_engine.get_field_filters()
		return frappe.render_template('kensingtonbn/templates/includes/filters.html',dict(filters = filters))
