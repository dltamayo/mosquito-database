#!/bin/bash

# Prompt the user to enter a password
read -sp 'Enter password: ' password

# Generate the SHA-256 hash of the password
hashed_password=$(echo -n "$password" | sha256sum | awk '{print $1}')

# Print the hashed password
echo
echo "SHA-256 hashed password: $hashed_password"
