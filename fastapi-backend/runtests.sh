#!/bin/bash

echo "Running FastAPI Backend Tests with Coverage"
echo "==========================================="

# Install dependencies if needed
pip3 install -r requirements.txt

# Clean up previous coverage data
rm -f .coverage
rm -rf htmlcov/

# Run tests with coverage
echo -e "\n📊 Running tests with coverage..."
python3 -m pytest tests/ --cov=. --cov-report=term-missing --cov-report=html --cov-report=xml -v

# Check if tests passed
if [ $? -eq 0 ]; then
    echo -e "\n✅ Tests passed!"
    
    # Display coverage summary
    echo -e "\n📈 Coverage Summary:"
    python3 -m coverage report
    
    # Generate detailed HTML report
    echo -e "\n📁 HTML coverage report generated in ./htmlcov/"
    echo "   To view the report, run: python3 -m http.server 8080 --directory htmlcov/"
    echo "   Or open: $BROWSER $(pwd)/htmlcov/index.html"
    
    # Optional: Open coverage report in browser automatically
    if command -v xdg-open &> /dev/null; then
        echo -e "\n🌐 Opening coverage report in browser..."
        xdg-open htmlcov/index.html
    elif [ -n "$BROWSER" ]; then
        "$BROWSER" "file://$(pwd)/htmlcov/index.html"
    fi
else
    echo -e "\n❌ Tests failed!"
    exit 1
fi