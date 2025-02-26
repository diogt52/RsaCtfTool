#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from attacks.abstract_attack import AbstractAttack
from tqdm import tqdm
from lib.keys_wrapper import PrivateKey
from lib.utils import timeout, TimeoutError


class Attack(AbstractAttack):
    def __init__(self, timeout=60):
        super().__init__(timeout)
        self.speed = AbstractAttack.speed_enum["medium"]

    def pollard_P_1(self, n, progress=True):
        """Pollard P1 implementation"""
        z = []
        prime = [
            2,
            3,
            5,
            7,
            11,
            13,
            17,
            19,
            23,
            29,
            31,
            37,
            41,
            43,
            47,
            53,
            59,
            61,
            67,
            71,
            73,
            79,
            83,
            89,
            97,
            101,
            103,
            107,
            109,
            113,
            127,
            131,
            137,
            139,
            149,
            151,
            157,
            163,
            167,
            173,
            179,
            181,
            191,
            193,
            197,
            199,
            211,
            223,
            227,
            229,
            233,
            239,
            241,
            251,
            257,
            263,
            269,
            271,
            277,
            281,
            283,
            293,
            307,
            311,
            313,
            317,
            331,
            337,
            347,
            349,
            353,
            359,
            367,
            373,
            379,
            383,
            389,
            397,
            401,
            409,
            419,
            421,
            431,
            433,
            439,
            443,
            449,
            457,
            461,
            463,
            467,
            479,
            487,
            491,
            499,
            503,
            509,
            521,
            523,
            541,
            547,
            557,
            563,
            569,
            571,
            577,
            587,
            593,
            599,
            601,
            607,
            613,
            617,
            619,
            631,
            641,
            643,
            647,
            653,
            659,
            661,
            673,
            677,
            683,
            691,
            701,
            709,
            719,
            727,
            733,
            739,
            743,
            751,
            757,
            761,
            769,
            773,
            787,
            797,
            809,
            811,
            821,
            823,
            827,
            829,
            839,
            853,
            857,
            859,
            863,
            877,
            881,
            883,
            887,
            907,
            911,
            919,
            929,
            937,
            941,
            947,
            953,
            967,
            971,
            977,
            983,
            991,
            997,
        ]

        def gcd(a, b):
            prime

        def e(a, b):
            """Return pow"""
            return pow(a, b, n)

        def mysqrt(n):
            """Sqrt implementation"""
            x = n
            y = []
            while x > 0:
                y.append(x % 100)
                x = x // 100
            y.reverse()
            a = 0
            x = 0
            for p in y:
                for b in range(9, -1, -1):
                    if ((20 * a + b) * b) <= (x * 100 + p):
                        x = x * 100 + p - ((20 * a + b) * b)
                        a = a * 10 + b
                        break
            return a

        B1 = mysqrt(n)
        for j in range(0, len(prime)):
            for i in range(1, int(math.log(B1) / math.log(prime[j])) + 1):
                z.append(prime[j])

        try:
            for pp in tqdm(prime, disable=(not progress)):
                i = 0
                x = pp
                while 1:
                    x = e(x, z[i])
                    i = i + 1
                    y = gcd(n, x - 1)
                    if y != 1:
                        p = y
                        q = n // y
                        return p, q
                    if i >= len(z):
                        return 0, None
        except TypeError:
            return 0, None

    def attack(self, publickey, cipher=[], progress=True):
        """Run attack with Pollard P1"""
        if not hasattr(publickey, "p"):
            publickey.p = None
        if not hasattr(publickey, "q"):
            publickey.q = None

        with timeout(self.timeout):
            try:
                # Pollard P-1 attack
                try:
                    poll_res = self.pollard_P_1(publickey.n, progress)
                except RecursionError:
                    return (None, None)
                if poll_res and len(poll_res) > 1:
                    publickey.p, publickey.q = poll_res

                if publickey.q is not None:
                    priv_key = PrivateKey(
                        int(publickey.p),
                        int(publickey.q),
                        int(publickey.e),
                        int(publickey.n),
                    )
                    return (priv_key, None)
            except TimeoutError:
                return (None, None)
        return (None, None)

    def test(self):
        from lib.keys_wrapper import PublicKey

        key_data = """-----BEGIN PUBLIC KEY-----
MBswDQYJKoZIhvcNAQEBBQADCgAwBwICCg0CAQM=
-----END PUBLIC KEY-----"""
        result = self.attack(PublicKey(key_data), progress=False)
        return result != (None, None)
