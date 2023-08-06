#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

"""BIP32 Hierarchical Deterministic Wallet functions.

A deterministic wallet is a hash-chain of private/public key pairs that
derives from a single root, which is the only element requiring backup.
Moreover, there are schemes where public keys can be calculated without
accessing private keys.

A hierarchical deterministic wallet is a tree of multiple hash-chains,
derived from a single root, allowing for selective sharing of keypair
chains.

Here, the HD wallet is implemented according to BIP32 bitcoin standard
https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki.
"""

from hashlib import sha512
from hmac import HMAC
from typing import Dict, List, Optional, Sequence, Tuple, Union

from .address import p2pkh_address
from .base58 import b58decode, b58encode
from .curvemult import mult
from .curves import secp256k1 as ec
from .segwitaddress import p2wpkh_address, p2wpkh_p2sh_address
from .utils import (Octets, bytes_from_hexstring, hash160, int_from_octets,
                    octets_from_point, point_from_octets)
from .wif import wif_from_prvkey

# Bitcoin core uses the m/0h (core) BIP32 derivation path
# with xprv/xpub and tprv/tpub Base58 encoding

# VERSION BYTES (4 bytes)

# m/44h/0h  p2pkh or p2sh
MAIN_xprv = b'\x04\x88\xAD\xE4'
MAIN_xpub = b'\x04\x88\xB2\x1E'
# m/44h/1h  p2pkh or p2sh
TEST_tprv = b'\x04\x35\x83\x94'
TEST_tpub = b'\x04\x35\x87\xCF'

# m/49h/0h  p2wpkh-p2sh (p2sh-wrapped-segwit)
MAIN_yprv = b'\x04\x9D\x78\x78'
MAIN_ypub = b'\x04\x9D\x7C\xB2'
# m/49h/1h  p2wpkh-p2sh (p2sh-wrapped-segwit)
TEST_uprv = b'\x04\x4A\x4E\x28'
TEST_upub = b'\x04\x4A\x52\x62'

#   ---     p2wsh-p2sh (p2sh-wrapped-segwit)
MAIN_Yprv = b'\x02\x95\xB0\x05'
MAIN_Ypub = b'\x02\x95\xB4\x3F'
TEST_Uprv = b'\x02\x42\x85\xB5'
TEST_Upub = b'\x02\x42\x89\xEF'

# m/84h/0h  p2wpkh (native-segwit)
MAIN_zprv = b'\x04\xB2\x43\x0C'
MAIN_zpub = b'\x04\xB2\x47\x46'
# m/84h/1h  p2wpkh (native-segwit)
TEST_vprv = b'\x04\x5F\x18\xBC'
TEST_vpub = b'\x04\x5F\x1C\xF6'

#   ---     p2wsh (native-segwit)
MAIN_Zprv = b'\x02\xAA\x7A\x99'
MAIN_Zpub = b'\x02\xAA\x7E\xD3'
TEST_Vprv = b'\x02\x57\x50\x48'
TEST_Vpub = b'\x02\x57\x54\x83'

_REPEATED_NETWORKS = [
    'mainnet', 'mainnet', 'mainnet', 'mainnet', 'mainnet',
    'testnet', 'testnet', 'testnet', 'testnet', 'testnet',
    'regtest', 'regtest', 'regtest', 'regtest', 'regtest']
_PRV_VERSIONS = [
    MAIN_xprv, MAIN_yprv, MAIN_zprv, MAIN_Yprv, MAIN_Zprv,
    TEST_tprv, TEST_uprv, TEST_vprv, TEST_Uprv, TEST_Vprv,
    TEST_tprv, TEST_uprv, TEST_vprv, TEST_Uprv, TEST_Vprv]
_PUB_VERSIONS = [
    MAIN_xpub, MAIN_ypub, MAIN_zpub, MAIN_Ypub, MAIN_Zpub,
    TEST_tpub, TEST_upub, TEST_vpub, TEST_Upub, TEST_Vpub,
    TEST_tpub, TEST_upub, TEST_vpub, TEST_Upub, TEST_Vpub]

_NETWORKS = ['mainnet', 'testnet', 'regtest']
# p2pkh or p2sh
_XPRV_PREFIXES = [MAIN_xprv, TEST_tprv, TEST_tprv]
_XPUB_PREFIXES = [MAIN_xpub, TEST_tpub, TEST_tpub]
# p2wpkh p2sh-wrapped-segwit
_P2WPKH_P2SH_PRV_PREFIXES = [MAIN_yprv, TEST_uprv, TEST_uprv]
_P2WPKH_P2SH_PUB_PREFIXES = [MAIN_ypub, TEST_upub, TEST_upub]
# p2wsh p2sh-wrapped-segwit
_P2WSH_P2SH_PRV_PREFIXES = [MAIN_Yprv, TEST_Uprv, TEST_Uprv]
_P2WSH_P2SH_PUB_PREFIXES = [MAIN_Ypub, TEST_Upub, TEST_Upub]
# p2wpkh native-segwit
_P2WPKH_PRV_PREFIXES = [MAIN_zprv, TEST_vprv, TEST_vprv]
_P2WPKH_PUB_PREFIXES = [MAIN_zpub, TEST_vpub, TEST_vpub]
# p2wsh native-segwit
_P2WSH_PRV_PREFIXES = [MAIN_Zprv, TEST_Vprv, TEST_Vprv]
_P2WSH_PUB_PREFIXES = [MAIN_Zpub, TEST_Vpub, TEST_Vpub]


# [  : 4] version
# [ 4: 5] depth
# [ 5: 9] parent_fingerprint
# [ 9:13] index
# [13:45] chain_code
# [45:78] key (private/public)

def _check_version_key(v: bytes, k: bytes) -> None:
    if not isinstance(k, bytes):
        msg = f"invalid key type: must be bytes, not '{type(k).__name__}'"
        raise TypeError(msg)
    if len(k) != 33:
        raise ValueError(f"invalid {len(k)}-bytes key length")

    if v in _PRV_VERSIONS:
        if k[0] != 0:
            raise ValueError("prvversion/pubkey mismatch")
    elif v in _PUB_VERSIONS:
        if k[0] not in (2, 3):
            raise ValueError("pubversion/prvkey mismatch")
    else:
        raise ValueError("unknown extended key version")


def _check_depth_fingerprint_index(d: int, f: bytes, i: bytes) -> None:
    if not isinstance(f, bytes):
        msg = "invalid parent_fingerprint type: "
        msg += f"must be bytes, not '{type(f).__name__}'"
        raise TypeError(msg)
    if len(f) != 4:
        raise ValueError(f"invalid {len(f)}-bytes parent_fingerprint length")

    if not isinstance(i, bytes):
        msg = "invalid index type: "
        msg += f"must be bytes, not '{type(i).__name__}'"
        raise TypeError(msg)
    if len(i) != 4:
        raise ValueError(f"invalid {len(i)}-bytes index length")

    if d < 0 or d > 255:
        raise ValueError(f"invalid depth ({d})")
    elif d == 0:
        if f != b'\x00\x00\x00\x00':
            msg = f"zero depth with non-zero parent_fingerprint {f!r}"
            raise ValueError(msg)
        if i != b'\x00\x00\x00\x00':
            msg = f"zero depth with non-zero index {i!r}"
            raise ValueError(msg)
    else:
        if f == b'\x00\x00\x00\x00':
            msg = f"non-zero depth ({d}) with zero parent_fingerprint {f!r}"
            raise ValueError(msg)


def parse(xkey: Octets) -> Dict:

    xkey = b58decode(xkey, 78)
    d = {
        'version'            : xkey[:4],
        'depth'              : xkey[4],
        'parent_fingerprint' : xkey[5:9],
        'index'              : xkey[9:13],
        'chain_code'         : xkey[13:45],
        'key'                : xkey[45:]
    }
    # coherence checks
    _check_version_key(d['version'], d['key'])
    _check_depth_fingerprint_index(d['depth'],
                                   d['parent_fingerprint'], d['index'])
    return d


def serialize(d: Dict) -> bytes:

    # coherence checks
    _check_version_key(d['version'], d['key'])
    _check_depth_fingerprint_index(d['depth'],
                                   d['parent_fingerprint'], d['index'])
    t = d['version']
    t += d['depth'].to_bytes(1, 'big')
    t += d['parent_fingerprint']
    t += d['index']

    chain_code = d['chain_code']
    if not isinstance(chain_code, bytes):
        msg = "invalid chain_code type: "
        msg += f"must be bytes, not '{type(chain_code).__name__}'"
        raise TypeError(msg)
    if len(chain_code) != 32:
        raise ValueError(f"invalid {len(chain_code)}-bytes chain_code length")
    t += chain_code

    t += d['key']

    return b58encode(t)


def parent_fingerprint(xkey: Octets) -> bytes:
    d = parse(xkey)
    if d['depth'] == 0:
        raise ValueError("master key provided")
    return d['parent_fingerprint']


def index(xkey: Octets) -> bytes:
    d = parse(xkey)
    if d['depth'] == 0:
        raise ValueError("master key provided")
    return d['index']


def fingerprint(xkey: Octets) -> bytes:
    d = parse(xkey)
    if d['key'][0] == 0:
        P = mult(int_from_octets(d['key'][1:]))
        d['key'] = octets_from_point(P, True, ec)
    return hash160(d['key'])[:4]


def address_from_xpub(xpub: Octets) -> bytes:
    """Return the address according to the xpub SLIP32 version type."""

    d = parse(xpub)

    if d['key'][0] not in (2, 3):
        raise ValueError("xkey is not a public one")

    if d['version'] in _XPUB_PREFIXES:
        # p2pkh
        return _p2pkh_address_from_xpub(d['version'], d['key'])
    elif d['version'] in _P2WPKH_PUB_PREFIXES:
        # p2wpkh native-segwit
        return _p2wpkh_address_from_xpub(d['version'], d['key'])
    else:
        # v in _P2WPKH_P2SH_PUB_PREFIXES
        # p2wpkh p2sh-wrapped-segwit
        return _p2wpkh_p2sh_address_from_xpub(d['version'], d['key'])


def wif_from_xprv(xprv: Octets, compressed: bool = True) -> bytes:
    """Return the WIF according to xpub version type."""

    d = parse(xprv)

    if d['key'][0] != 0:
        raise ValueError("xkey is not a private one")

    network = _REPEATED_NETWORKS[_PRV_VERSIONS.index(d['version'])]
    return wif_from_prvkey(d['key'][1:], compressed, network)


def _p2pkh_address_from_xpub(v: bytes, pk: bytes) -> bytes:
    network = _REPEATED_NETWORKS[_PUB_VERSIONS.index(v)]
    return p2pkh_address(pk, network)


def p2pkh_address_from_xpub(xpub: Octets) -> bytes:
    """Return the p2pkh address."""
    d = parse(xpub)
    if d['key'][0] not in (2, 3):
        # Deriving pubkey from prvkey would not be enough:
        # compressed ot uncompressed?
        raise ValueError("xkey is not a public one")
    return _p2pkh_address_from_xpub(d['version'], d['key'])


def _p2wpkh_address_from_xpub(v: bytes, pk: bytes) -> bytes:
    network = _REPEATED_NETWORKS[_PUB_VERSIONS.index(v)]
    return p2wpkh_address(pk, network)


def p2wpkh_address_from_xpub(xpub: Octets) -> bytes:
    """Return the p2wpkh (native SegWit) address."""
    d = parse(xpub)
    if d['key'][0] not in (2, 3):
        # if pubkey would be derived from prvkey,
        # then this safety check might be removed
        raise ValueError("xkey is not a public one")
    return _p2wpkh_address_from_xpub(d['version'], d['key'])


def _p2wpkh_p2sh_address_from_xpub(v: bytes, pk: bytes) -> bytes:
    network = _REPEATED_NETWORKS[_PUB_VERSIONS.index(v)]
    return p2wpkh_p2sh_address(pk, network)


def p2wpkh_p2sh_address_from_xpub(xpub: Octets) -> bytes:
    """Return the p2wpkh p2sh-wrapped (legacy) address."""
    d = parse(xpub)
    if d['key'][0] not in (2, 3):
        # if pubkey would be derived from prvkey,
        # then this safety check might be removed
        raise ValueError("xkey is not a public one")
    return _p2wpkh_p2sh_address_from_xpub(d['version'], d['key'])


def rootxprv_from_seed(seed: Octets, version: Octets = MAIN_xprv) -> bytes:
    """derive the BIP32 root master extended private key from the seed"""

    seed = bytes_from_hexstring(seed)
    hd = HMAC(b"Bitcoin seed", seed, sha512).digest()
    d = {
        'version'            : bytes_from_hexstring(version),
        'depth'              : 0,
        'parent_fingerprint' : b'\x00\x00\x00\x00',
        'index'              : b'\x00\x00\x00\x00',
        'chain_code'         : hd[32:],
        'key'                : b'\x00' + hd[:32]
    }
    return serialize(d)


def xpub_from_xprv(xprv: Octets) -> bytes:
    """Neutered Derivation (ND).

    Derivation of the extended public key corresponding to an extended
    private key (“neutered” as it removes the ability to sign transactions).
    """

    d = parse(xprv)

    if d['key'][0] != 0:
        raise ValueError("extended key is not a private one")
    P = mult(int_from_octets(d['key'][1:]))
    d['key'] = octets_from_point(P, True, ec)

    d['version'] = _PUB_VERSIONS[_PRV_VERSIONS.index(d['version'])]

    return serialize(d)


def ckd(xparentkey: Octets, index: Union[Octets, int]) -> bytes:
    """Child Key Derivation (CDK)

    Key derivation is normal if the extended parent key is public or
    index is less than 0x80000000.

    Key derivation is hardened if the extended parent key is private and
    index is not less than 0x80000000.
    """

    d = parse(xparentkey)
    _ckd(d, index)
    return serialize(d)


def _ckd(d: Dict, index: Union[Octets, int]) -> None:
    if isinstance(index, int):
        index = index.to_bytes(4, byteorder='big')

    index = bytes_from_hexstring(index)

    if len(index) != 4:
        raise ValueError(f"a 4 bytes int is required, not {len(index)}")

    d['depth'] += 1

    if d['key'][0] == 0:                             # parent is a prvkey
        parent = int.from_bytes(d['key'][1:], byteorder='big')
        Parent = mult(parent)
        Parent_bytes = octets_from_point(Parent, True, ec)
    else:                                            # parent is a pubkey
        Parent = point_from_octets(d['key'], ec)
        Parent_bytes = d['key']
        if index[0] >= 0x80:                         # hardened derivation
            raise ValueError("hardened derivation from pubkey is impossible")
    d['parent_fingerprint'] = hash160(Parent_bytes)[:4]
    d['index'] = index

    if d['key'][0] == 0:                             # parent is a prvkey
        if index[0] >= 0x80:                         # hardened derivation
            h = HMAC(d['chain_code'], d['key'] + index, sha512).digest()
        else:                                        # normal derivation
            h = HMAC(d['chain_code'], Parent_bytes + index, sha512).digest()
        d['chain_code'] = h[32:]
        offset = int.from_bytes(h[:32], byteorder='big')
        child = (parent + offset) % ec.n
        d['key'] = b'\x00' + child.to_bytes(32, 'big')
    else:                                            # parent is a pubkey
        h = HMAC(d['chain_code'], d['key'] + index, sha512).digest()
        d['chain_code'] = h[32:]
        offset = int.from_bytes(h[:32], byteorder='big')
        Offset = mult(offset)
        Child = ec.add(Parent, Offset)
        d['key'] = octets_from_point(Child, True, ec)


def _indexes_from_path(path: str) -> Tuple[Sequence[int], bool]:
    """Extract derivation indexes from a derivation path.

    Derivation path must be like "m/44'/0'/1'/0/10" (absolute)
    or "./0/10" (relative).
    """

    steps = path.split('/')
    if steps[0] in ('m', 'M'):
        absolute = True
    elif steps[0] == '.':
        absolute = False
    elif steps[0] == '':
        raise ValueError('Empty derivation path')
    else:
        raise ValueError(f'Invalid derivation path root: "{steps[0]}"')
    if len(steps) > 256:
        raise ValueError(f'Derivation path depth {len(steps)-1}>255')

    indexes: List[int] = list()
    for step in steps[1:]:
        hardened = False
        if step[-1] in ("'", "H", "h"):
            hardened = True
            step = step[:-1]
        index = int(step)
        index += 0x80000000 if hardened else 0
        indexes.append(index)

    return indexes, absolute


def derive(xkey: Octets, path: Union[str, Sequence[int]]) -> bytes:
    """Derive an extended key.

    Derivation is according to absolute path like "m/44h/0'/1H/0/10"
    or relative path like "./0/10".
    """

    d = parse(xkey)

    if isinstance(path, str):
        path = path.strip()
        indexes, absolute = _indexes_from_path(path)
        if absolute and d["depth"] != 0:
            msg = "Absolute derivation path for non-root master key"
            raise ValueError(msg)
    else:
        indexes = path

    final_depth = d["depth"] + len(indexes)
    if final_depth > 255:
        raise ValueError(f'Derivation path final depth {final_depth}>255')

    for index in indexes:
        _ckd(d, index)

    return serialize(d)


def crack(parent_xpub: Octets, child_xprv: Octets) -> bytes:
    p = parse(parent_xpub)

    if p['key'][0] not in (2, 3):
        raise ValueError("extended parent key is not a public one")

    c = parse(child_xprv)
    if c['key'][0] != 0:
        raise ValueError("extended child key is not a private one")

    # check depth
    if c['depth'] != p['depth'] + 1:
        raise ValueError("not a parent's child: wrong depth relation")

    # check fingerprint
    if c['parent_fingerprint'] != hash160(p['key'])[:4]:
        raise ValueError("not a parent's child: wrong parent fingerprint")

    # check normal derivation
    if c['index'][0] >= 0x80:
        raise ValueError("hardened child derivation")

    p['version'] = c['version']

    h = HMAC(p['chain_code'], p['key'] + c['index'], sha512).digest()
    offset = int.from_bytes(h[:32], byteorder='big')
    child = int.from_bytes(c['key'][1:], byteorder='big')
    parent = (child - offset) % ec.n
    Parent_b = b'\x00' + parent.to_bytes(32, byteorder='big')
    p['key'] = Parent_b

    return serialize(p)
