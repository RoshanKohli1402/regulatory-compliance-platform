#!/bin/bash

echo "🌍 Global Regulatory Compliance Auditor - Setup"
echo "================================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "⚠️  Could not create virtual environment. Installing globally..."
else
    echo "✅ Virtual environment created"
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate
fi

echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Create directories
echo "📁 Creating directories..."
mkdir -p models
mkdir -p regulations

echo "✅ Directories created"
echo ""

# Check for regulation files
echo "🔍 Checking regulation configurations..."
reg_count=$(ls regulations/*.json 2>/dev/null | grep -v "_TEMPLATE" | wc -l)

if [ $reg_count -eq 0 ]; then
    echo "⚠️  No regulation configurations found in regulations/"
    echo "   Please add regulation JSON files to the regulations/ directory"
else
    echo "✅ Found $reg_count regulation configuration(s)"
fi

echo ""

# Success message
echo "================================================"
echo "✨ Setup Complete!"
echo ""
echo "🚀 To start the application:"
echo "   1. Activate environment: source venv/bin/activate"
echo "   2. Start backend: python app.py"
echo "   3. Open frontend.html in your browser"
echo ""
echo "📚 For more information, see README.md"
echo "================================================"
