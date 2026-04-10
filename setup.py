#!/usr/bin/env python3
"""
Setup script for the Adaptive Learning System MVP.
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is sufficient."""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def install_dependencies():
    """Install required Python packages."""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Set up environment variables."""
    print("\nSetting up environment...")
    
    # Check if .env file exists
    if os.path.exists(".env"):
        print("✓ .env file already exists")
        return True
    
    # Create .env from .env.example if it exists
    if os.path.exists(".env.example"):
        try:
            with open(".env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())
            print("✓ Created .env file from .env.example")
            print("  Please edit .env and add your OpenAI API key")
            return True
        except Exception as e:
            print(f"✗ Failed to create .env file: {e}")
            return False
    else:
        print("✗ .env.example not found")
        print("  Please create a .env file with OPENAI_API_KEY=your_key_here")
        return False

def verify_structure():
    """Verify the project structure."""
    print("\nVerifying project structure...")
    
    required_files = [
        "knowledge_graph.json",
        "question_bank.json",
        "llm_evaluator.py",
        "mastery_evaluator.py",
        "prerequisite_checker.py",
        "test_pipeline.py",
        "main.py",
        "requirements.txt",
        "README.md"
    ]
    
    all_good = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} (missing)")
            all_good = False
    
    return all_good

def main():
    """Main setup function."""
    print("=" * 60)
    print("ADAPTIVE LEARNING SYSTEM MVP - SETUP")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Verify structure
    if not verify_structure():
        print("\nSome files are missing. Please ensure you have all project files.")
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        response = input("\nContinue without installing dependencies? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Edit the .env file and add your OpenAI API key")
    print("2. Run the system: python main.py")
    print("3. Or run the test pipeline: python test_pipeline.py")
    print("\nNote: Without an OpenAI API key, the system will use mock evaluations.")
    
    # Ask if user wants to run the demo
    response = input("\nRun demo now? (y/n): ").strip().lower()
    if response == 'y':
        print("\nStarting demo...")
        import main
        main.main()

if __name__ == "__main__":
    main()