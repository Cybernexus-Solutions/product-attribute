import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    
    _logger.info("=== PRODUCT SEQUENCE PRE-MIGRATION: Starting product default code validation ===")

    cr.execute("""
        SELECT id FROM product_product
        WHERE default_code IS NULL OR default_code = ''
    """)
    products_without_default_code = cr.fetchall()
    count = len(products_without_default_code)

    for product_id, in products_without_default_code:
        new_default_code = f"PROD-{product_id}"
        _logger.info(f"Setting default_code for product {product_id} to {new_default_code}")
        cr.execute("""
            UPDATE product_product
            SET default_code = %s
            WHERE id = %s
        """, (new_default_code, product_id))

    util.add_to_migration_reports(
        f"- Set `default_code` for {count} product(s) missing it (format: `PROD-<id>`)",
        category="product_sequence",
        format="md",
    )

    _logger.info("=== PRODUCT SEQUENCE PRE-MIGRATION: Product default code validation complete ===")
