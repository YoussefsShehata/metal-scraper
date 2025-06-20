import os, sys
# Add the project root (one level up) to sys.path so pytest can import app.*
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
