#!/bin/bash

# Choralink Easy Arranger Script
# Makes it simple to create arrangements without remembering commands

echo "🎼 Welcome to Choralink Easy Arranger!"
echo "======================================"
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Function to display menu
show_menu() {
    echo "What would you like to do?"
    echo "1) Create a simple arrangement"
    echo "2) Create arrangement with custom difficulty"
    echo "3) Create arrangement with transposition"
    echo "4) Show help"
    echo "5) Exit"
    echo ""
}

# Function to select instrument
select_instrument() {
    echo "Select an instrument:"
    echo "1) Saxophone"
    echo "2) Trumpet"
    echo "3) Flute"
    echo "4) Clarinet"
    echo "5) Piano"
    echo ""
    read -p "Enter choice (1-5): " instrument_choice
    
    case $instrument_choice in
        1) INSTRUMENT="saxophone";;
        2) INSTRUMENT="trumpet";;
        3) INSTRUMENT="flute";;
        4) INSTRUMENT="clarinet";;
        5) INSTRUMENT="piano";;
        *) echo "Invalid choice, using saxophone"; INSTRUMENT="saxophone";;
    esac
}

# Function to select difficulty
select_difficulty() {
    echo "Select difficulty level:"
    echo "1) Beginner"
    echo "2) Intermediate"
    echo "3) Advanced"
    echo "4) Virtuoso"
    echo ""
    read -p "Enter choice (1-4): " diff_choice
    
    case $diff_choice in
        1) DIFFICULTY="beginner";;
        2) DIFFICULTY="intermediate";;
        3) DIFFICULTY="advanced";;
        4) DIFFICULTY="virtuoso";;
        *) echo "Invalid choice, using intermediate"; DIFFICULTY="intermediate";;
    esac
}

# Main loop
while true; do
    show_menu
    read -p "Enter your choice (1-5): " choice
    
    case $choice in
        1)
            # Simple arrangement
            read -p "Enter the path to your music file: " INPUT_FILE
            if [ ! -f "$INPUT_FILE" ]; then
                echo "❌ File not found: $INPUT_FILE"
                continue
            fi
            select_instrument
            echo "Creating arrangement..."
            $PYTHON_CMD backend/run_choralink.py --input "$INPUT_FILE" --instrument "$INSTRUMENT"
            echo "✅ Done! Check for the output file in the same directory as your input."
            echo ""
            ;;
            
        2)
            # With difficulty
            read -p "Enter the path to your music file: " INPUT_FILE
            if [ ! -f "$INPUT_FILE" ]; then
                echo "❌ File not found: $INPUT_FILE"
                continue
            fi
            select_instrument
            select_difficulty
            echo "Creating arrangement..."
            $PYTHON_CMD backend/run_choralink.py --input "$INPUT_FILE" --instrument "$INSTRUMENT" --difficulty "$DIFFICULTY"
            echo "✅ Done! Check for the output file in the same directory as your input."
            echo ""
            ;;
            
        3)
            # With transposition
            read -p "Enter the path to your music file: " INPUT_FILE
            if [ ! -f "$INPUT_FILE" ]; then
                echo "❌ File not found: $INPUT_FILE"
                continue
            fi
            select_instrument
            select_difficulty
            read -p "Enter target key (e.g., Bb, Eb, F): " KEY
            echo "Creating arrangement..."
            $PYTHON_CMD backend/run_choralink.py --input "$INPUT_FILE" --instrument "$INSTRUMENT" --difficulty "$DIFFICULTY" --key "$KEY"
            echo "✅ Done! Check for the output file in the same directory as your input."
            echo ""
            ;;
            
        4)
            # Show help
            $PYTHON_CMD backend/run_choralink.py --help
            echo ""
            ;;
            
        5)
            # Exit
            echo "Thank you for using Choralink! 🎵"
            exit 0
            ;;
            
        *)
            echo "Invalid choice. Please try again."
            echo ""
            ;;
    esac
done