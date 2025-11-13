#!/bin/bash

# Quick Start Script for Login System

echo "==================================="
echo "Login System - Quick Start"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found"

# Install requirements
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Run the application
echo ""
echo "🚀 Starting the application..."
echo "📱 The app will open at: http://localhost:8501"
echo ""
streamlit run frontend.py
