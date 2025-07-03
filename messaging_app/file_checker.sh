#!/bin/bash

# Check if ingress.yaml exists and is not empty
if [ ! -f "messaging_app/ingress.yaml" ]; then
    echo "❌ Error: ingress.yaml is missing"
    exit 1
elif [ ! -s "messaging_app/ingress.yaml" ]; then
    echo "❌ Error: ingress.yaml exists but is empty"
    exit 1
else
    echo "✅ ingress.yaml exists and contains content"
fi

# Check if commands.txt exists and is not empty
if [ ! -f "messaging_app/commands.txt" ]; then
    echo "❌ Error: commands.txt is missing"
    exit 1
elif [ ! -s "messaging_app/commands.txt" ]; then
    echo "❌ Error: commands.txt exists but is empty"
    exit 1
else
    echo "✅ commands.txt exists and contains content"
fi

exit 0
