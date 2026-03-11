#!/usr/bin/env python3
"""Test sensor connections"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

async def test_geophone():
    """Test geophone array"""
    try:
        from instruments.litho_geo_v2 import GeophoneArray
        geo = GeophoneArray()
        data = await geo.read()
        print(f"✅ Geophone array: {data.shape} samples")
        return True
    except Exception as e:
        print(f"❌ Geophone array: {e}")
        return False

async def test_infrasound():
    """Test infrasound array"""
    try:
        from instruments.infrasound_array import InfrasoundArray
        inf = InfrasoundArray()
        data = await inf.read()
        print(f"✅ Infrasound array: {data.shape} samples")
        return True
    except Exception as e:
        print(f"❌ Infrasound array: {e}")
        return False

async def test_tiltmeter():
    """Test tiltmeter"""
    try:
        from instruments.tiltmeter import Tiltmeter
        tilt = Tiltmeter()
        data = await tilt.read()
        print(f"✅ Tiltmeter: {data.shape} samples")
        return True
    except Exception as e:
        print(f"❌ Tiltmeter: {e}")
        return False

async def test_all():
    """Test all sensors"""
    results = await asyncio.gather(
        test_geophone(),
        test_infrasound(),
        test_tiltmeter()
    )
    
    success = all(results)
    print(f"\n{'✅' if success else '❌'} All tests: {'PASSED' if success else 'FAILED'}")
    return success

if __name__ == "__main__":
    asyncio.run(test_all())
