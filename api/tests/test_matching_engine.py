"""
Test Cases for Updated Matching Engine
Tests threshold-based matching and AND/OR logic
"""

import json
from api.services.matching_engine import MatchingEngine

class BusinessDetails:
    """Simple business details class for testing"""
    def __init__(self, size_sqm, seating_capacity, features=None):
        self.size_sqm = size_sqm
        self.seating_capacity = seating_capacity
        self.features = features or []
        
        # Calculate size category (for legacy matching)
        if size_sqm <= 50:
            self.size_category = "small"
        elif size_sqm <= 100:
            self.size_category = "medium"
        else:
            self.size_category = "large"

def load_regulations():
    """Load updated regulations"""
    import os
    file_path = os.path.join(os.path.dirname(__file__), '..', 'regulations_updated.json')
    with open(os.path.abspath(file_path), 'r', encoding='utf-8') as f:

        data = json.load(f)
    return data['regulations']

def test_matching_engine():
    """Run comprehensive tests"""
    
    engine = MatchingEngine()
    regulations = load_regulations()
    
    print("=" * 80)
    print("🧪 MATCHING ENGINE TEST SUITE")
    print("=" * 80)
    
    # Test Case 1: Small restaurant (should NOT get REG-027 or REG-028)
    print("\n📋 TEST 1: Small Restaurant")
    print("-" * 80)
    business1 = BusinessDetails(size_sqm=40, seating_capacity=30, features=['delivery'])
    matched1 = engine.match_regulations(business1, regulations)
    
    has_027 = any(r['id'] == 'REG-027' for r in matched1)
    has_028 = any(r['id'] == 'REG-028' for r in matched1)
    
    print(f"   Size: {business1.size_sqm} sqm, Seating: {business1.seating_capacity}")
    print(f"   Features: {business1.features}")
    print(f"   Total Regulations: {len(matched1)}")
    print(f"   ✓ REG-027 (Fire Detection): {'❌ MATCHED (WRONG!)' if has_027 else '✅ NOT matched (correct)'}")
    print(f"   ✓ REG-028 (Sprinklers): {'❌ MATCHED (WRONG!)' if has_028 else '✅ NOT matched (correct)'}")
    
    # Test Case 2: Medium restaurant (should get REG-027, NOT REG-028)
    print("\n📋 TEST 2: Medium Restaurant")
    print("-" * 80)
    business2 = BusinessDetails(size_sqm=80, seating_capacity=60, features=['alcohol'])
    matched2 = engine.match_regulations(business2, regulations)
    
    has_027 = any(r['id'] == 'REG-027' for r in matched2)
    has_028 = any(r['id'] == 'REG-028' for r in matched2)
    has_004 = any(r['id'] == 'REG-004' for r in matched2)
    
    print(f"   Size: {business2.size_sqm} sqm, Seating: {business2.seating_capacity}")
    print(f"   Features: {business2.features}")
    print(f"   Total Regulations: {len(matched2)}")
    print(f"   ✓ REG-027 (Fire Detection): {'✅ MATCHED (correct - >50 OR logic)' if has_027 else '❌ NOT matched (WRONG!)'}")
    print(f"   ✓ REG-028 (Sprinklers): {'❌ MATCHED (WRONG!)' if has_028 else '✅ NOT matched (correct)'}")
    print(f"   ✓ REG-004 (Alcohol to Minors): {'✅ MATCHED (correct - has alcohol)' if has_004 else '❌ NOT matched (WRONG!)'}")
    
    # Test Case 3: Large restaurant (should get BOTH REG-027 and REG-028)
    print("\n📋 TEST 3: Very Large Restaurant")
    print("-" * 80)
    business3 = BusinessDetails(size_sqm=350, seating_capacity=350, features=['alcohol', 'live_music'])
    matched3 = engine.match_regulations(business3, regulations)
    
    has_027 = any(r['id'] == 'REG-027' for r in matched3)
    has_028 = any(r['id'] == 'REG-028' for r in matched3)
    
    print(f"   Size: {business3.size_sqm} sqm, Seating: {business3.seating_capacity}")
    print(f"   Features: {business3.features}")
    print(f"   Total Regulations: {len(matched3)}")
    print(f"   ✓ REG-027 (Fire Detection): {'✅ MATCHED (correct - >50)' if has_027 else '❌ NOT matched (WRONG!)'}")
    print(f"   ✓ REG-028 (Sprinklers): {'✅ MATCHED (correct - >301 AND >300)' if has_028 else '❌ NOT matched (WRONG!)'}")
    
    # Test Case 4: Edge case - exactly at threshold
    print("\n📋 TEST 4: Edge Case - Exactly 50 sqm, 50 seats")
    print("-" * 80)
    business4 = BusinessDetails(size_sqm=50, seating_capacity=50, features=[])
    matched4 = engine.match_regulations(business4, regulations)
    
    has_027 = any(r['id'] == 'REG-027' for r in matched4)
    
    print(f"   Size: {business4.size_sqm} sqm, Seating: {business4.seating_capacity}")
    print(f"   Features: {business4.features}")
    print(f"   Total Regulations: {len(matched4)}")
    print(f"   ✓ REG-027 (Fire Detection): {'✅ MATCHED (correct - >=50)' if has_027 else '❌ NOT matched (WRONG!)'}")
    
    # Test Case 5: Outdoor + Alcohol (should get REG-030)
    print("\n📋 TEST 5: Outdoor Seating with Alcohol")
    print("-" * 80)
    business5 = BusinessDetails(size_sqm=70, seating_capacity=40, features=['outdoor', 'alcohol'])
    matched5 = engine.match_regulations(business5, regulations)
    
    has_030 = any(r['id'] == 'REG-030' for r in matched5)
    has_004 = any(r['id'] == 'REG-004' for r in matched5)
    
    print(f"   Size: {business5.size_sqm} sqm, Seating: {business5.seating_capacity}")
    print(f"   Features: {business5.features}")
    print(f"   Total Regulations: {len(matched5)}")
    print(f"   ✓ REG-030 (Outdoor+Alcohol): {'✅ MATCHED (correct - has both)' if has_030 else '❌ NOT matched (WRONG!)'}")
    print(f"   ✓ REG-004 (Alcohol to Minors): {'✅ MATCHED (correct - has alcohol)' if has_004 else '❌ NOT matched (WRONG!)'}")
    
    # Test Case 6: Outdoor only (should NOT get REG-030)
    print("\n📋 TEST 6: Outdoor Seating WITHOUT Alcohol")
    print("-" * 80)
    business6 = BusinessDetails(size_sqm=70, seating_capacity=40, features=['outdoor'])
    matched6 = engine.match_regulations(business6, regulations)
    
    has_030 = any(r['id'] == 'REG-030' for r in matched6)
    has_004 = any(r['id'] == 'REG-004' for r in matched6)
    
    print(f"   Size: {business6.size_sqm} sqm, Seating: {business6.seating_capacity}")
    print(f"   Features: {business6.features}")
    print(f"   Total Regulations: {len(matched6)}")
    print(f"   ✓ REG-030 (Outdoor+Alcohol): {'❌ MATCHED (WRONG!)' if has_030 else '✅ NOT matched (correct - needs both)'}")
    print(f"   ✓ REG-004 (Alcohol to Minors): {'❌ MATCHED (WRONG!)' if has_004 else '✅ NOT matched (correct - no alcohol)'}")
    
    # Test Case 7: Large size but small seating (should NOT get REG-028)
    print("\n📋 TEST 7: Large Space, Small Seating")
    print("-" * 80)
    business7 = BusinessDetails(size_sqm=350, seating_capacity=80, features=['kitchen_gas'])
    matched7 = engine.match_regulations(business7, regulations)
    
    has_027 = any(r['id'] == 'REG-027' for r in matched7)
    has_028 = any(r['id'] == 'REG-028' for r in matched7)
    
    print(f"   Size: {business7.size_sqm} sqm, Seating: {business7.seating_capacity}")
    print(f"   Features: {business7.features}")
    print(f"   Total Regulations: {len(matched7)}")
    print(f"   ✓ REG-027 (Fire Detection): {'✅ MATCHED (correct - >50 either)' if has_027 else '❌ NOT matched (WRONG!)'}")
    print(f"   ✓ REG-028 (Sprinklers): {'❌ MATCHED (WRONG!)' if has_028 else '✅ NOT matched (correct - needs 300+ seats too)'}")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    
    print(f"\nAlways-required regulations (should appear in all tests):")
    always_reqs = [r for r in regulations if r['applicable_conditions'].get('always_required')]
    print(f"   Found: {len(always_reqs)} regulations")
    for reg in always_reqs[:5]:  # Show first 5
        print(f"   - {reg['id']}: {reg['title']}")
    if len(always_reqs) > 5:
        print(f"   ... and {len(always_reqs) - 5} more")
    
    print(f"\n🎯 Critical Tests:")
    print(f"   1. Small business (40 sqm, 30 seats): ✅ Passed" if not any(r['id'] in ['REG-027', 'REG-028'] for r in matched1) else "   1. Small business: ❌ FAILED")
    print(f"   2. Medium business (80 sqm, 60 seats): ✅ Passed" if any(r['id'] == 'REG-027' for r in matched2) and not any(r['id'] == 'REG-028' for r in matched2) else "   2. Medium business: ❌ FAILED")
    print(f"   3. Very large (350 sqm, 350 seats): ✅ Passed" if any(r['id'] == 'REG-028' for r in matched3) else "   3. Very large business: ❌ FAILED")
    print(f"   4. Outdoor + Alcohol: ✅ Passed" if any(r['id'] == 'REG-030' for r in matched5) else "   4. Outdoor + Alcohol: ❌ FAILED")
    print(f"   5. Outdoor only: ✅ Passed" if not any(r['id'] == 'REG-030' for r in matched6) else "   5. Outdoor only: ❌ FAILED")
    print(f"   6. Large space, small seating: ✅ Passed" if not any(r['id'] == 'REG-028' for r in matched7) else "   6. Large space, small seating: ❌ FAILED")
    
    print("\n" + "=" * 80)
    print("✅ TEST SUITE COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_matching_engine()