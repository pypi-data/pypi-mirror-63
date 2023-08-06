# Copyright (c) 2017 Pieter Wuille
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Copyright (C) 2019-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.


"""SegWit address functions.

Some of these functions were originally from
https://github.com/sipa/bech32/tree/master/ref/python,
with the following modifications:

* moved bech32 stuff into bech32.py
* type annotated python3
* avoided returning None or (None, None), throwing ValueError instead
* detailed error messages and exteded safety checks
* check that bech32 addresses are not longer than 90 characters
  (as this is not enforced by bech32._encode anymore)
"""


from typing import Iterable, List, Tuple, Union

from .bech32 import b32decode, b32encode
from .address import p2sh_address
from .script import Token, encode
from .utils import Octets, bytes_from_hexstring, hash160, sha256

WitnessProgram = Union[List[int], bytes]

_NETWORKS = ['mainnet', 'testnet', 'regtest']
_P2W_PREFIXES = ['bc', 'tb', 'bcrt']


def has_segwit_prefix(addr: Union[str, bytes]) -> bool:

    if isinstance(addr, bytes):
        str_addr = addr.decode()
    else:
        str_addr = addr.strip()
        str_addr = str_addr.lower()
    
    for prefix in _P2W_PREFIXES:
        if str_addr.startswith(prefix + '1'):
            return True

    return False


def _convertbits(data: Iterable[int], frombits: int,
                 tobits: int, pad: bool = True) -> List[int]:
    """General power-of-2 base conversion."""
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            raise ValueError(f"invalid value {value}")
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)

    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        raise ValueError("failure")

    return ret


def _check_witness(witvers: int, witprog: WitnessProgram):
    l = len(witprog)
    if witvers == 0:
        if l != 20 and l != 32:
            raise ValueError(f"witness program length ({l}) is not 20 or 32")
    elif witvers > 16 or witvers < 0:
        msg = f"witness version ({witvers}) not in [0, 16]"
        raise ValueError(msg)
    else:
        if l < 2 or l > 40:
            raise ValueError(f"witness program length ({l}) not in [2, 40]")


def _decode(address: Union[str, bytes]) -> Tuple[str, int, List[int]]:
    """Decode a SegWit address."""

    if isinstance(address, str):
        address = address.strip()

    # the following check was originally in b32decode
    # but it does not pertain there
    if len(address) > 90:
        raise ValueError(f"Bech32 address length ({len(address)}) > 90")

    hrp, data = b32decode(address)

    # check that it is a SegWit address
    i = _P2W_PREFIXES.index(hrp)

    if len(data) == 0:
        raise ValueError(f"Bech32 address with empty data")

    witvers = data[0]
    witprog = _convertbits(data[1:], 5, 8, False)
    _check_witness(witvers, witprog)

    return _NETWORKS[i], witvers, witprog


def _encode(network: str, wv: int, wp: WitnessProgram) -> bytes:
    """Encode a SegWit address."""

    _check_witness(wv, wp)
    hrp = _P2W_PREFIXES[_NETWORKS.index(network)]
    ret = b32encode(hrp, [wv] + _convertbits(wp, 8, 5))
    return ret


def _p2wpkh_address(h160: bytes, native: bool, network: str) -> bytes:
    """Return the p2wpkh address as native SegWit or legacy p2sh-wrapped."""

    if len(h160) != 20:
        msg = f"Witness program length ({len(h160)}) "
        msg += "is not 20-bytes"
        raise ValueError(msg)
    witvers = 0
    if native:
        return _encode(network, witvers, h160)
    # script_pubkey = [0, key_hash], i.e. 0x0014{20-byte key-hash}
    script_pubkey = b'\x00\x14' + h160
    return p2sh_address(script_pubkey, network)


def _h160_pubkey(pubkey: Octets) -> bytes:
    pubkey = bytes_from_hexstring(pubkey)
    if pubkey[0] not in (2, 3):
        raise ValueError(f"Uncompressed pubkey {pubkey.hex()}")
    psize = 32  # FIXME: parametrize on network
    if len(pubkey) != psize + 1:
        msg = f"Wrong pubkey size: {len(pubkey)} instead of {psize + 1}"
        raise ValueError(msg)
    return hash160(pubkey)


def p2wpkh_address(pubkey: Octets, network: str = 'mainnet') -> bytes:
    """Return the p2wpkh native SegWit address."""
    native = True
    return _p2wpkh_address(_h160_pubkey(pubkey), native, network)


def p2wpkh_p2sh_address(pubkey: Octets, network: str = 'mainnet') -> bytes:
    """Return the p2wpkh-p2sh (legacy) address."""
    native = False
    return _p2wpkh_address(_h160_pubkey(pubkey), native, network)


def _p2wsh_address(h256: bytes, native: bool, network: str) -> bytes:
    """Return the address as native SegWit bech32 or legacy p2sh-wrapped."""

    if len(h256) != 32:
        raise ValueError(f"witness program length ({len(h256)}) is not 32")
    witvers = 0
    if native:
        return _encode(network, witvers, h256)

    script_pubkey: List[Token] = [witvers, h256]
    return p2sh_address(encode(script_pubkey), network)


def p2wsh_address(wscript: Octets, network: str = 'mainnet') -> bytes:
    """Return the p2wsh native SegWit address."""
    native = True
    return _p2wsh_address(sha256(wscript), native, network)


def p2wsh_p2sh_address(wscript: Octets, network: str = 'mainnet') -> bytes:
    """Return the p2wsh-p2sh (legacy) address."""
    native = False
    return _p2wsh_address(sha256(wscript), native, network)


def hash_from_bech32_address(address: Union[str, bytes]) -> Tuple[str, bool, bytes]:

    network, wv, wp = _decode(address)
    if wv != 0:
        raise ValueError(f"Invalid witness version: {wv}")
    if len(wp) == 20:
        is_script_hash = False
    else:
        is_script_hash = True

    return network, is_script_hash, bytes(wp)
