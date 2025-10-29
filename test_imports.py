"""
Basic import test for PyDayflow
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        # Core imports
        from pydayflow.utils.config import Config
        print("✓ Config module")
        
        from pydayflow.models.database import DatabaseManager, Recording, TimelineCard
        print("✓ Database models")
        
        # No external dependencies needed for these
        print("\nAll basic imports successful!")
        print("\nNote: Full functionality requires installing dependencies from requirements.txt")
        return True
        
    except Exception as e:
        print(f"✗ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
