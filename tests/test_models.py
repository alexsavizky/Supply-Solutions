"""
Module docstring: This module contains unit tests for the models module.
"""

import unittest

from models import User, Supply, SupplyList


class TestUser(unittest.TestCase):
    def test_insert(self):
        user = User()
        user.insert('test@example.com', 'password', 'John', 'Doe')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.password, 'password')
        self.assertEqual(user.name, 'John')
        self.assertEqual(user.lastname, 'Doe')

    def test_tupple_insert(self):
        user = User()
        user.tupple_insert((1, 'test@example.com', 'password', 1, 'John', 'Doe'))
        self.assertEqual(user.id, 1)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.password, 'password')
        self.assertEqual(user.type, 1)
        self.assertEqual(user.name, 'John')
        self.assertEqual(user.lastname, 'Doe')

    def test_totuple(self):
        user = User()
        user.insert('test@example.com', 'password', 'John', 'Doe')
        self.assertEqual(user.totuple(), ('test@example.com', 'password', 1, 'John', 'Doe'))


class TestSupply(unittest.TestCase):
    def test_insert(self):
        supply = Supply()
        supply.insert(1, 'type', 'name', 10, 5, 'desc', 0)
        self.assertEqual(supply.id, 1)
        self.assertEqual(supply.type, 'type')
        self.assertEqual(supply.name, 'name')
        self.assertEqual(supply.all_units, 10)
        self.assertEqual(supply.available_units, 5)
        self.assertEqual(supply.description, 'desc')
        self.assertEqual(supply.broken_units, 0)

    def test_tupple_insert(self):
        supply = Supply()
        supply.tupple_insert((1, 'name', 10, 5, 'type', 'desc', 0))
        self.assertEqual(supply.id, 1)
        self.assertEqual(supply.name, 'name')
        self.assertEqual(supply.all_units, 10)
        self.assertEqual(supply.available_units, 5)
        self.assertEqual(supply.type, 'type')
        self.assertEqual(supply.description, 'desc')
        self.assertEqual(supply.broken_units, 0)

    def test_borrow(self):
        supply = Supply()
        supply.insert(1, 'type', 'name', 10, 5, 'desc', 0)
        self.assertEqual(supply.borrow(3), 2)
        self.assertEqual(supply.borrow(5), False)

    def test_return_item(self):
        supply = Supply()
        supply.insert(1, 'type', 'name', 10, 5, 'desc', 0)
        self.assertEqual(supply.return_item(2), 7)

    def test_totuple(self):
        supply = Supply()
        supply.insert(1, 'type', 'name', 10, 5, 'desc', 0)
        self.assertEqual(supply.totuple(), (1, 'name', 10, 5, 'type', 'desc', 0))


class TestSupplyList(unittest.TestCase):
    def test_insert_list(self):
        supply_list = SupplyList()
        supply_list.insert_list([(1, 'name1', 10, 5, 'type1', 'desc', 0), (2, 'name2', 15, 7, 'type2', 'desc', 0)])
        self.assertEqual(len(supply_list.list), 2)

    def test_borrow_item_by_id(self):
        supply_list = SupplyList()
        supply_list.insert_list([(1, 'name1', 10, 5, 'type1', 'desc', 0), (2, 'name2', 15, 7, 'type2', 'desc', 0)])
        self.assertEqual(supply_list.borrow_item_by_id(1, 3), 2)
        self.assertEqual(supply_list.borrow_item_by_id(1, 6), False)

    def test_return_item_by_id(self):
        supply_list = SupplyList()
        supply_list.insert_list([(1, 'name1', 10, 5, 'type1', 'desc', 0), (2, 'name2', 15, 7, 'type2', 'desc', 0)])
        self.assertEqual(supply_list.return_item_by_id(2, 3), 10)

    def test_get_avl_item_by_id(self):
        supply_list = SupplyList()
        supply_list.insert_list([(1, 'name1', 10, 5, 'type1', 'desc', 0), (2, 'name2', 15, 7, 'type2', 'desc', 0)])
        self.assertEqual(supply_list.get_avl_item_by_id(2), 7)
        self.assertEqual(supply_list.get_avl_item_by_id(3), False)

    def test_get_items_names(self):
        supply_list = SupplyList()
        supply_list.insert_list([(1, 'name1', 10, 5, 'type1', 'desc', 0), (2, 'name2', 15, 7, 'type2', 'desc', 0)])
        self.assertEqual(supply_list.get_items_names(), ['name1', 'name2'])

    def test_get_id_by_name(self):
        supply_list = SupplyList()
        supply_list.insert_list([(1, 'name1', 10, 5, 'type1', 'desc', 0), (2, 'name2', 15, 7, 'type2', 'desc', 0)])
        self.assertEqual(supply_list.get_id_by_name('name2'), 2)
        self.assertEqual(supply_list.get_id_by_name('name3'), False)

    def test_get_supply_avl_by_name(self):
        supply_list = SupplyList()
        supply_list.insert_list([(1, 'name1', 10, 5, 'type1', 'desc', 0), (2, 'name2', 15, 7, 'type2', 'desc', 0)])
        self.assertEqual(supply_list.get_supply_avl_by_name('name2'), 7)
        self.assertEqual(supply_list.get_supply_avl_by_name('name3'), None)

    def test_get_name_by_id(self):
        supply_list = SupplyList()
        supply_list.insert_list([(1, 'name1', 10, 5, 'type1', 'desc', 0), (2, 'name2', 15, 7, 'type2', 'desc', 0)])
        self.assertEqual(supply_list.get_name_by_id(1), 'name1')
        self.assertEqual(supply_list.get_name_by_id(3), False)


if __name__ == '__main__':
    unittest.main()
