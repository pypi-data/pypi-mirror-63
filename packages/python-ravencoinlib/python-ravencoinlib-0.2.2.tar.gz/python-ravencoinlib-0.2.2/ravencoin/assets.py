# Copyright (C) 2018-2020 The python-ravencoinlib developers
#
# This file is part of python-ravencoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-ravencoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

"""Ravencoin assets"""

from __future__ import absolute_import, division, print_function, unicode_literals

import re

MAX_NAME_LENGTH = 30  # +1 for admin

sha_256_hash = re.compile("^[A-Fa-f0-9]{64}$")  # regex matching a sha256 hash

ROOT_NAME_CHARACTERS = re.compile(r"^[A-Z0-9._]{3,}$")
SUB_NAME_CHARACTERS = re.compile(r"^[A-Z0-9._]+$")
UNIQUE_TAG_CHARACTERS = re.compile(r"^[-A-Za-z0-9@$%&*()[\]{}_.?:]+$")
CHANNEL_TAG_CHARACTERS = re.compile(r"^[A-Z0-9._]+$")
VOTE_TAG_CHARACTERS = re.compile(r"^[A-Z0-9._]+$")

QUALIFIER_NAME_CHARACTERS = re.compile(r"^[A-Z0-9._]{3,}$")
SUB_QUALIFIER_NAME_CHARACTERS = re.compile(r"^[A-Z0-9._]+$")
RESTRICTED_NAME_CHARACTERS = re.compile(r"^[A-Z0-9._]{3,}$")

DOUBLE_PUNCTUATION = re.compile(r"^.*[._]{2,}.*$")
LEADING_PUNCTUATION = re.compile(r"^[._].*$")
TRAILING_PUNCTUATION = re.compile(r"^.*[._]$")

RAVEN_NAMES = re.compile("^RVN$|^RAVEN$|^RAVENCOIN$")


class InvalidAssetName(Exception):
    pass


class InvalidAssetType(Exception):
    pass


# Asset name representation
# Types: CMainAsset, CSubAsset, CUniqueAsset
# if admin == True, then this represents the admin token (ends with '!')

class CAsset(object):
    # parent class for asset types
    # don't use this directly, use one of the subclasses instead
    def __init__(self, name, parent=None, admin=False, *, ownership=None):
        if ownership is not None:
            # for backwards compatibility with < v0.2
            # ownership is alias for admin
            admin = ownership
        if type(admin) is not bool:
            raise TypeError("CAsset __init__: admin={} must be of type bool".format(admin))
        self.admin = admin
        self.parent = parent
        self.name = name

    @property
    def full_name(self):
        if isinstance(self, CMainAsset):
            return self._name
        elif isinstance(self, CRestrictedAsset):
            return "$" + self._name
        elif isinstance(self, CSubAsset):
            return self.parent.full_name + '/' + self._name
        elif isinstance(self, CUniqueAsset):
            return self.parent.full_name + '#' + self._name
        elif isinstance(self, CSubQualifierTag):
            return self.parent.full_name + '/#' + self._name
        elif isinstance(self, CQualifierTag):
            return '#' + self._name
        else:
            return self._name

    def __str__(self):
        return self.full_name

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if parent is not None and parent.admin is True:
            raise InvalidAssetType("Can't set admin token as parent")
        self._parent = parent

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, namestr):
        # check for invalid asset name

        if RAVEN_NAMES.match(namestr):
            raise InvalidAssetName("not allowed (RVN/RAVEN/RAVENCOIN")
        if DOUBLE_PUNCTUATION.match(namestr):
            raise InvalidAssetName("double punctuation")
        if LEADING_PUNCTUATION.match(namestr):
            raise InvalidAssetName("leading punctuation")
        if TRAILING_PUNCTUATION.match(namestr):
            raise InvalidAssetName("trailing punctuation")
        if isinstance(self, CMainAsset) and not ROOT_NAME_CHARACTERS.match(namestr):
            raise InvalidAssetName(
                "\nInvalid characters in asset name {}\n('A-Z', '0-9' '.' and '_' allowed, uppercase only, min length 3)".format(
                    namestr))
        elif isinstance(self, CSubAsset) and not SUB_NAME_CHARACTERS.match(namestr):
            raise InvalidAssetName(
                "\nInvalid characters in asset name {}\n('A-Z', '0-9' '.' and '_' allowed, uppercase only".format(
                    namestr))
        elif isinstance(self, CUniqueAsset) and not UNIQUE_TAG_CHARACTERS.match(namestr):
            raise InvalidAssetName("\nInvalid characters in asset name {}\n".format(
                namestr) + "'A-Z', 'a-z', '0-9' '-@$%&*()[]{}_.?:' allowed")
        if isinstance(self, CRestrictedAsset) and not RESTRICTED_NAME_CHARACTERS.match(namestr):
            raise InvalidAssetName(
                "\nInvalid characters in restricted asset name {}\n('A-Z', '0-9' '.' and '_' allowed, uppercase only, min length 3)".format(
                    namestr))
        if isinstance(self, CQualifierTag) and not QUALIFIER_NAME_CHARACTERS.match(namestr):
            raise InvalidAssetName(
                "\nInvalid characters in qualifier name {}\n('A-Z', '0-9' '.' and '_' allowed, uppercase only, min length 3)".format(
                    namestr))

        max_length = MAX_NAME_LENGTH
        if self.admin:
            if not namestr.endswith('!'):
                namestr = namestr + '!'
            max_length += 1

        self._name = namestr

        # unique tag '#' is not counted when checking length, as raven source
        if len(self.full_name.replace('#', '')) > max_length:
            raise InvalidAssetName("Asset string {} is too long (max {} characters)".format(self.full_name, max_length))


class CMainAsset(CAsset):
    def __init__(self, name, admin=False, *, ownership=None):
        if ownership is not None:
            admin = ownership
        super(CMainAsset, self).__init__(name, admin=admin)


class CSubAsset(CAsset):
    def __init__(self, name, parent=None, admin=False, *, ownership=None):
        if ownership is not None:
            admin = ownership
        if parent is None:
            raise InvalidAssetType("CSubAsset parent not provided")
        if isinstance(parent, CMainAsset) or isinstance(parent, CSubAsset):
            super(CSubAsset, self).__init__(name, parent=parent, admin=admin)
        else:
            raise InvalidAssetType("CSubAsset requires parent of type CMainAsset or CSubAsset")


class CUniqueAsset(CAsset):
    def __init__(self, name, parent=None):
        if parent == None:
            raise InvalidAssetType("CUniqueAsset parent not provided")
        if isinstance(parent, CMainAsset) or isinstance(parent, CSubAsset):
            super(CUniqueAsset, self).__init__(name, parent=parent)
        else:
            raise InvalidAssetType("CUniqueAsset requires parent of type CMainAsset or CSubAsset")

    def __str__(self):
        return self.name

class CRestrictedAsset(CAsset):
    def __init__(self, name, admin=False):
        super(CRestrictedAsset, self).__init__(name, admin=admin)

class CQualifierTag(CAsset):
    def __init__(self, name, admin=False):
        super(CQualifierTag, self).__init__(name, admin=admin)

class CSubQualifierTag(CAsset):
    def __init__(self, name,parent=None,admin=False):
        if parent is None:
            raise InvalidAssetType("CSubQualifier parent not provided")
        if isinstance(parent, CQualifierTag):
            super(CSubQualifierTag, self).__init__(name, parent=parent, admin=admin)
        else:
            raise InvalidAssetType("CSubQualifierTag requires parent of type CQualifierTag")


def split_asset_name(s):
    # split an asset string into list of parts

    if s.startswith('$'): # restricted asset
        return [CRestrictedAsset(s[1:])]

    if s.startswith('#'): # qualifier tag
        if s.count('#') == 1:
            return [CQualifierTag(s[1:])]

        result = []
        prev = None
        s = s.replace('/','/\xfa')
        split_l = re.split('/',s)
        for part in split_l:
            if part.startswith('\xfa'):
                a = CSubQualifierTag(part[2:], parent=prev)
                result.append(a)
                prev = a
            else:
                a = CQualifierTag(part[1:])
                result.append(a)
                prev = a
        return result

    s = s.replace('/','/\xfa') # hack, re.split excludes delimiter from results, so double it up with a placeholder
    s = s.replace('#','#\xfb')
    s = s.replace('~','~\xfc')
    split_l = re.split('/|#|~',s)

    result = []
    prev = None
    for part in split_l:
        admin = part.endswith('!')
        if admin:
            part = part.rsplit('!')[0]
        if part.startswith('\xfb'):
            a = CUniqueAsset(part[1:], parent=prev)
            result.append(a)
            prev = a
        elif part.startswith('\xfa'):
            a = CSubAsset(part[1:], parent=prev, admin=admin)
            result.append(a)
            prev = a
        elif part.startswith('\xfc'):
            a = CMessageChannel(part[1:],parent=prev)
            result.append(a)
            prev = a
        else:
            a = CMainAsset(part, admin=admin)
            result.append(a)
            prev = a
    return result


class CAssetName(object):
    def __init__(self,s=""):
        self.parts = []

        if len(s) < 3:
            raise InvalidAssetName("Asset name {} is too short".format(s))

        self.parts = split_asset_name(s)

    def __str__(self):
        if len(self.parts) > 0:
            last = self.parts[-1]
            return last.full_name
        else:
            return ""


# Asset metadata representation
# https://github.com/RavenProject/Ravencoin/blob/master/assets/asset_metadata_spec.md

class Asset_Metadata(object):
    def __init__(self, contract_url="", contract_hash="", contract_signature="",
                 contract_address="", symbol="", name="", issuer="", description="", description_mime="",
                 type="", website_url="", icon="", image_url="", contact_name="", contact_email="",
                 contact_address="", contact_phone="", forsale=None, forsale_price="", forsale_price_currency="",
                 restricted="", validate=True):

        self._validate = validate  # if True, attempt to validate fields

        self.contract_url = contract_url
        self.contract_hash = contract_hash
        self.contract_signature = contract_signature
        self.contract_address = contract_address
        self.symbol = symbol
        self.name = name
        self.issuer = issuer
        self.description = description
        self.description_mime = description_mime
        self.type = type
        self.website_url = website_url
        self.icon = icon
        self.image_url = image_url
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_address = contact_address
        self.contact_phone = contact_phone
        self.forsale = forsale
        # currency and price can be given separately
        # otherwise assume forsale_price is already formatted e.g. "1000 USD" as spec
        if (forsale_price != "") and (forsale_price_currency != ""):
            self.forsale_price = forsale_price + " " + forsale_price_currency
        else:
            self.forsale_price = forsale_price
        self.restricted = restricted

    def __str__(self):
        """ Returns json serializable string """
        import json
        return json.dumps(dict((key, value) for key, value in iter([
            ("contract_url", self.contract_url),
            ("contract_hash", self.contract_hash),
            ("contract_signature", self.contract_signature),
            ("contract_address", self.contract_address),
            ("symbol", self.symbol),
            ("name", self.name),
            ("issuer", self.issuer),
            ("description", self.description),
            ("description_mime", self.description_mime),
            ("type", self.type),
            ("website_url", self.website_url),
            ("icon", self.icon),
            ("image_url", self.image_url),
            ("contact_name", self.contact_name),
            ("contact_email", self.contact_email),
            ("contact_address", self.contact_address),
            ("contact_phone", self.contact_phone),
            ("forsale", self.forsale),
            ("forsale_price", self.forsale_price),
            ("restricted", self.restricted)
        ]) if value is not None and value != ""))

    @property
    def contract_hash(self):
        return self._contract_hash

    @contract_hash.setter
    def contract_hash(self, hashstr):
        if not self._validate or hashstr == "":
            self._contract_hash = hashstr
        else:
            if sha_256_hash.match(hashstr):
                self._contract_hash = hashstr
            else:
                raise ValueError("contract_hash must be a sha256 hash in ascii hex")

"""Ravencoin messaging"""

MAX_CHANNEL_NAME_LENGTH = 12

class InvalidChannelName(Exception):
    pass

class CMessageChannel(object):
    def __init__(self,name,parent=None):
        self.parent = parent
        self.name = name

    @property
    def full_name(self):
        return self.parent.full_name + '~' + self.name

    def __str__(self):
        return self.full_name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,namestr):
    # check for invalid channel name
        if len(namestr) > MAX_CHANNEL_NAME_LENGTH:
            raise InvalidChannelName("Channel name {} is too long (max {} characters)".format(namestr,MAX_CHANNEL_NAME_LENGTH))
        self._name = namestr
    # check full name "ASSET~CHANNEL" as well
        if len(str(self)) > MAX_NAME_LENGTH:
            raise InvalidChannelName("Channel name {} is too long (max {} characters)".format(str(self),MAX_NAME_LENGTH))

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self,parent):
        if parent is None or (not isinstance(parent, CMainAsset) and not isinstance(parent, CSubAsset)):
            raise InvalidChannelName("Messaging channel requires parent of type CMainAsset or CSubAsset")
        self._parent = parent

