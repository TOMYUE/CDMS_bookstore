import pytest
from be.relations.init import *

class TestCreateRelations:
    def test_create_relations(self):
        buyer_table = Table('Buyer', meta)
        assert insp.has_table(buyer_table) == True
        seller_table = Table('Seller', meta)
        assert insp.has_table(seller_table) == True
        store_table = Table('Store', meta)
        assert insp.has_table(store_table) == True
        deal_table = Table('Deal', meta)
        assert insp.has_table(deal_table) == True
        deal_book_table = Table('DealBook', meta)
        assert insp.has_table(deal_book_table) == True
        store_owner_table = Table('StoreOwner', meta)
        assert insp.has_table(store_owner_table) == True