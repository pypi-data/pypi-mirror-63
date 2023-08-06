"""Unit tests for OrderedBTreeFolder.

Repeat the unit tests for the normal BTreeFolder2 and additional tests
for the OrderSupport.
"""

import functools
import unittest
from Acquisition import aq_base
from OFS.ObjectManager import BadRequestException
from OFS.Folder import Folder
from Products.orderedbtreefolder.orderedbtreefolder import OrderedBTreeFolder
from Products.orderedbtreefolder.orderedbtreefolder import OBEND
from Products.BTreeFolder2.BTreeFolder2 import ExhaustedUniqueIdsError


class Tests(unittest.TestCase):

    def setUp(self):
        self.f = OrderedBTreeFolder('root')
        ff = OrderedBTreeFolder('item')
        self.f._setOb(ff.id, ff)
        self.ff = self.f._getOb(ff.id)

    def testAdded(self):
        self.assertEqual(self.ff.id, 'item')

    def testCount(self):
        self.assertEqual(self.f.objectCount(), 1)
        self.assertEqual(self.ff.objectCount(), 0)
        self.assertEqual(len(self.f), 1)
        self.assertEqual(len(self.ff), 0)

    def testObjectIds(self):
        self.assertEqual(list(self.f.objectIds()), ['item'])
        self.assertEqual(list(self.f.keys()), ['item'])
        self.assertEqual(list(self.ff.objectIds()), [])
        f3 = OrderedBTreeFolder('item3')
        self.f._setOb(f3.id, f3)
        lst = sorted(self.f.objectIds())
        self.assertEqual(lst, ['item', 'item3'])

    def testObjectIdsWithMetaType(self):
        f2 = Folder()
        f2.id = 'subfolder'
        self.f._setOb(f2.id, f2)
        mt1 = OrderedBTreeFolder.meta_type
        mt2 = Folder.meta_type
        self.assertEqual(list(self.f.objectIds(mt1)), ['item'])
        self.assertEqual(list(self.f.objectIds((mt1,))), ['item'])
        self.assertEqual(list(self.f.objectIds(mt2)), ['subfolder'])
        lst = sorted(self.f.objectIds([mt1, mt2]))
        self.assertEqual(lst, ['item', 'subfolder'])
        self.assertEqual(list(self.f.objectIds('blah')), [])

    def testObjectValues(self):
        values = self.f.objectValues()
        self.assertEqual(len(values), 1)
        self.assertEqual(values[0].id, 'item')
        # Make sure the object is wrapped.
        self.assertIsNot(values[0], aq_base(values[0]))

    def testObjectItems(self):
        items = self.f.objectItems()
        self.assertEqual(len(items), 1)
        id, val = items[0]
        self.assertEqual(id, 'item')
        self.assertEqual(val.id, 'item')
        # Make sure the object is wrapped.
        self.assertIsNot(val, aq_base(val))

    def testHasObject(self):
        self.assertTrue(self.f.hasObject('item'))
        self.assertIn('item', self.f)

    def testDelete(self):
        self.f._delOb('item')
        self.assertEqual(list(self.f.objectIds()), [])
        self.assertEqual(self.f.objectCount(), 0)

    def testObjectMap(self):
        map = self.f.objectMap()
        self.assertEqual(list(map), [{'id': 'item', 'meta_type':
                                      OrderedBTreeFolder.meta_type}])
        # I'm not sure why objectMap_d() exists, since it appears to be
        # the same as objectMap(), but it's implemented by Folder.
        self.assertEqual(list(self.f.objectMap_d()), list(self.f.objectMap()))

    def testObjectIds_d(self):
        self.assertEqual(self.f.objectIds_d(), {'item': 1})

    def testCheckId(self):
        self.assertEqual(self.f._checkId('xyz'), None)
        self.assertRaises(BadRequestException, self.f._checkId, 'item')
        self.assertRaises(BadRequestException, self.f._checkId, 'REQUEST')

    def testSetObject(self):
        f2 = OrderedBTreeFolder('item2')
        self.f._setObject(f2.id, f2)
        self.assertTrue(self.f.hasObject('item2'))
        self.assertEqual(self.f.objectCount(), 2)

    def testWrapped(self):
        base = aq_base(self.f._getOb('item'))
        self.assertIsNot(self.f._getOb('item'), base)
        self.assertIsNot(self.f['item'], base)
        self.assertIsNot(self.f.get('item'), base)
        self.assertIs(self.f._getOb('item').aq_base, base)

    def testGenerateId(self):
        ids = {}
        for n in range(10):
            ids[self.f.generateId()] = 1
        self.assertEqual(len(ids), 10)  # All unique
        for id in ids.keys():
            self.f._checkId(id)  # Must all be valid

    def testGenerateIdDenialOfServicePrevention(self):
        for n in range(10):
            item = Folder()
            item.id = 'item%d' % n
            self.f._setOb(item.id, item)
        self.f.generateId('item', rand_ceiling=20)  # Shouldn't be a problem
        self.assertRaises(ExhaustedUniqueIdsError,
                          self.f.generateId, 'item', rand_ceiling=9)

    def testReplace(self):
        old_f = Folder()
        old_f.id = 'item'
        inner_f = OrderedBTreeFolder('inner')
        old_f._setObject(inner_f.id, inner_f)
        self.ff._populateFromFolder(old_f)
        self.assertEqual(self.ff.objectCount(), 1)
        self.assertTrue(self.ff.hasObject('inner'))
        self.assertEqual(aq_base(self.ff._getOb('inner')), inner_f)

    def testObjectListing(self):
        f2 = OrderedBTreeFolder('somefolder')
        self.f._setObject(f2.id, f2)
        # Hack in an absolute_url() method that works without context.
        self.f.absolute_url = lambda: ''
        info = self.f.getBatchObjectListing()
        self.assertEqual(info['b_start'], 1)
        self.assertEqual(info['b_end'], 2)
        self.assertEqual(info['prev_batch_url'], '')
        self.assertEqual(info['next_batch_url'], '')
        self.assertGreater(info['formatted_list'].find('</select>'), 0)
        self.assertGreater(info['formatted_list'].find('item'), 0)
        self.assertGreater(info['formatted_list'].find('somefolder'), 0)

        # Ensure batching is working.
        info = self.f.getBatchObjectListing({'b_count': 1})
        self.assertEqual(info['b_start'], 1)
        self.assertEqual(info['b_end'], 1)
        self.assertEqual(info['prev_batch_url'], '')
        self.assertNotEqual(info['next_batch_url'], '')
        # change this, as objects are inserted at the beginning by default
        self.assertLess(info['formatted_list'].find('item'), 0)
        self.assertGreater(info['formatted_list'].find('somefolder'), 0)

        info = self.f.getBatchObjectListing({'b_start': 2})
        self.assertEqual(info['b_start'], 2)
        self.assertEqual(info['b_end'], 2)
        self.assertNotEqual(info['prev_batch_url'], '')
        self.assertEqual(info['next_batch_url'], '')
        # change this, as objects are inserted at the beginning by default
        self.assertGreater(info['formatted_list'].find('item'), 0)
        self.assertLess(info['formatted_list'].find('somefolder'), 0)

    def testCleanup(self):
        self.assertTrue(self.f._cleanup())
        key = TrojanKey('a')
        self.f._tree[key] = 'b'
        self.assertTrue(self.f._cleanup())
        key.value = 'z'

        # With a key in the wrong place, there should now be damage.
        self.assertFalse(self.f._cleanup())
        # Now it's fixed.
        self.assertTrue(self.f._cleanup())
        # Verify the management interface also works,
        # but don't test return values.
        self.f.manage_cleanup()
        key.value = 'a'
        self.f.manage_cleanup()

    # now test the order support
    def testOrdering(self):
        folder = self.f
        # there is already an object item in the folder
        self.f._delOb('item')
        self.assertEqual(list(self.f.objectIds()), [])
        self.assertEqual(self.f.objectCount(), 0)

        f1 = OrderedBTreeFolder('new1')
        folder._setObject(f1.getId(), f1)
        f2 = OrderedBTreeFolder('new2')
        folder._setObject(f2.getId(), f2)
        f3 = OrderedBTreeFolder('new3')
        folder._setObject(f3.getId(), f3)

        self.assertEqual(folder.getObjectPosition('new1'), 2)
        self.assertEqual(folder.getObjectPosition('new2'), 1)
        self.assertEqual(folder.getObjectPosition('new3'), 0)
        folder.moveObjectsToTop(['new1'])
        self.assertEqual(folder.getObjectPosition('new1'), 0)
        folder.moveObjectsToBottom(['new1'])
        self.assertEqual(folder.getObjectPosition('new1'), 2)

        # test: rotation does not happen
        folder.moveObjectsToBottom(['new1'])
        self.assertEqual(folder.getObjectPosition('new1'), 2)

        # add a new one to play with
        fx = OrderedBTreeFolder('new4')
        folder._setObject(fx.getId(), fx)

        self.assertEqual(folder.getObjectPosition('new4'), 0)
        folder.moveObjectsToTop(['new4'])
        self.assertEqual(folder.getObjectPosition('new4'), 0)

        # look if the order can be used
        self.assertEqual(folder.objectIds(), ['new4', 'new3', 'new2', 'new1'])
        self.assertEqual(list(folder.keys()), ['new4', 'new3', 'new2', 'new1'])
        self.assertEqual([x.getId() for x in folder.objectValues()],
                         ['new4', 'new3', 'new2', 'new1'])
        self.assertEqual([x.getId() for x in folder.values()],
                         ['new4', 'new3', 'new2', 'new1'])
        self.assertEqual([x[0] for x in folder.objectItems()],
                         ['new4', 'new3', 'new2', 'new1'])
        self.assertEqual([x[0] for x in folder.items()],
                         ['new4', 'new3', 'new2', 'new1'])

    def test_orderedbetreefolder__OrderSupport__moveObjectsByDelta__1(self):
        """It does not change order when moving an object out of the list."""
        self.f.insertmodus = OBEND
        self.f._setObject('item-2', OrderedBTreeFolder('item-2'))
        self.f._setObject('item-3', OrderedBTreeFolder('item-3'))
        self.f._setObject('item-4', OrderedBTreeFolder('item-4'))
        self.assertEqual(['item', 'item-2', 'item-3', 'item-4'], self.f.keys())
        self.f.moveObjectsByDelta('item', -1)
        self.assertEqual(['item', 'item-2', 'item-3', 'item-4'], self.f.keys())
        self.f.moveObjectsByDelta('item-4', 1)
        self.assertEqual(['item', 'item-2', 'item-3', 'item-4'], self.f.keys())


@functools.total_ordering
class TrojanKey:
    """Pretends to be a consistent, immutable, humble citizen...

    then sweeps the rug out from under the BTree.
    """

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        """We assume a string as type to compare against."""
        return self.value == other

    def __lt__(self, other):
        """We assume a string as type to compare against."""
        return self.value < other

    def __hash__(self):
        return hash(self.value)
