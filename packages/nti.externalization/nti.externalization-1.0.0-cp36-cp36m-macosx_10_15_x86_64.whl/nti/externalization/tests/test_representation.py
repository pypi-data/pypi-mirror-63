# -*- coding: utf-8 -*-
"""
Tests for representation.py

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# stdlib imports
import re
import unittest

from persistent import Persistent

import fudge

from . import ExternalizationLayerTest
from .. import representation

from hamcrest import assert_that
from hamcrest import contains_string
from hamcrest import is_

logger = __import__('logging').getLogger(__name__)

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904
# pylint:disable=attribute-defined-outside-init, useless-object-inheritance

class TestWithRepr(unittest.TestCase):

    def test_default(self):

        @representation.WithRepr
        class Foo(object):
            pass

        r = repr(Foo())
        assert_that(r, contains_string('<nti.externalization.tests.test_representation.Foo'))
        assert_that(r, contains_string('{}>'))

    def test_proxied(self):
        from zope.security.checker import ProxyFactory
        @representation.WithRepr
        class Foo(object):
            pass

        r = repr(ProxyFactory(Foo()))
        assert_that(r, contains_string('<nti.externalization.tests.test_representation.Foo at'))
        assert_that(r, contains_string('{}'))


    def test_with_default_callable(self):
        @representation.WithRepr(lambda s: "<HI>")
        class Foo(object):
            pass

        r = repr(Foo())
        assert_that(r, is_("<HI>"))

    def test_raises_POSError(self):
        def raise_(self):
            from ZODB.POSException import ConnectionStateError
            raise ConnectionStateError()

        @representation.WithRepr(raise_)
        class Foo(object):
            pass

        r = repr(Foo())
        assert_that(r,
                    is_("<nti.externalization.tests.test_representation.Foo(Ghost, "
                        "ConnectionStateError())>"))

    def test_raises_attribute_error(self):
        def raise_(self):
            raise AttributeError()

        @representation.WithRepr(raise_)
        class Foo(object):
            pass

        r = repr(Foo())
        assert_that(r,
                    is_("<nti.externalization.tests.test_representation.Foo("
                        "AttributeError())>"))

    def _normalize_repr(self, r):
        # Pure-python vs C
        r = r.replace('nti.externalization.tests.test_representation.', '')
        # addresses
        r = re.sub(r'0x[0-9a-fA-F]*', '0xdeadbeef', r)
        # Python 3.7 removed the trailing , in exception reprs
        r = r.replace("',)", "')")
        # Python 2 doesn't have a leading b prefix for byte literals
        r = r.replace("oid '", "oid b'")
        return r

    def _normalized_repr(self, o):
        return self._normalize_repr(repr(o))

    def test_persistent_subclass_default(self):
        @representation.WithRepr
        class Foo(Persistent):
            pass

        o = Foo()
        r = self._normalized_repr(o)

        assert_that(r,
                    is_('<Foo object at 0xdeadbeef _p_repr {}>'))

        o._p_oid = b'12345678'
        r = self._normalized_repr(o)
        # Persistent 4.4.3 and above represent the OID using hex; prior
        # to that it was bytes.
        assert_that(r,
                    is_("<Foo object at 0xdeadbeef oid 0xdeadbeef _p_repr {}>"))

        o.a = 1

        r = self._normalized_repr(o)

        assert_that(r,
                    is_("<Foo object at 0xdeadbeef oid 0xdeadbeef _p_repr {'a': 1}>"))

    def test_persistent_subclass_custom(self):
        @representation.WithRepr(lambda s: 'Hi')
        class Foo(Persistent):
            pass

        o = Foo()
        r = self._normalized_repr(o)
        assert_that(r,
                    is_('<Foo object at 0xdeadbeef _p_repr Hi>'))

    def test_persistent_subclass_raise(self):

        def raise_(self):
            raise AttributeError()

        @representation.WithRepr(raise_)
        class Foo(Persistent):
            pass

        o = Foo()
        r = self._normalized_repr(o)

        assert_that(r,
                    is_('<Foo object at 0xdeadbeef _p_repr AttributeError()>'))


class TestYaml(unittest.TestCase):

    def test_unicode(self):
        yaml = representation.YamlRepresenter()

        result = yaml.dump(u"Hi")
        assert_that(result, is_('Hi\n...\n'))

        result = yaml.load(result)
        assert_that(result, is_(u'Hi'))

class TestJson(ExternalizationLayerTest):

    def test_dump_to_stream(self):
        import io

        json = representation.JsonRepresenter()
        bio = io.BytesIO() if str is bytes else io.StringIO()
        json.dump(u"hi", bio)

        assert_that(bio.getvalue(), is_('"hi"'))

    def test_load_bytes(self):
        json = representation.JsonRepresenter()
        result = json.load(b'"hi"')
        assert_that(result, is_(u"hi"))

    @fudge.patch('simplejson.loads')
    def test_loads_returns_bytes(self, loads):
        loads.expects_call().returns(b'bytes')

        json = representation.JsonRepresenter()
        result = json.load(b'hi')
        assert_that(result, is_(u'bytes'))


    def test_to_json_representation(self):
        result = representation.to_json_representation({})
        assert_that(result, is_('{}'))

    def test_second_pass(self):
        from ..interfaces import IExternalObject
        from zope import component

        json = representation.JsonRepresenter()
        result = json.dump(self)
        assert_that(result, contains_string('NonExternalizableObject'))

        class SecondPass(object):

            def __init__(self, obj):
                self.obj = obj

            def toExternalObject(self, **kw):
                return self.obj

        component.getGlobalSiteManager().registerAdapter(
            SecondPass,
            required=(type(self,),),
            provided=IExternalObject,
            name="second-pass"
        )



        json = representation.JsonRepresenter()
        with self.assertRaises(TypeError):
            json.dump(self)

        component.getGlobalSiteManager().unregisterAdapter(
            SecondPass,
            required=(type(self,),),
            provided=IExternalObject,
            name="second-pass"
        )
