#!/bin/bash

# Function to check Python version
check_python_version() {
    # Check for Python version
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    if [[ "$PYTHON_VERSION" == 3.10* || "$PYTHON_VERSION" == 3.11* || "$PYTHON_VERSION" == 3.12* ]]; then
        echo "Python version $PYTHON_VERSION is supported."
    else
        echo "Unsupported Python version: $PYTHON_VERSION. Please install Python 3.10, 3.11, or 3.12."
        exit 1
    fi
}

# Function to check Git installation
check_git_installation() {
    if ! git --version &> /dev/null; then
        echo "Git is not installed. Please install Git."
        exit 1
    else
        echo "Git is installed."
    fi
}

# Function to check Poetry installation
check_poetry_installation() {
    if ! poetry --version &> /dev/null; then
        echo "Poetry is not installed. Please install Poetry."
        exit 1
    else
        echo "Poetry is installed."
    fi
}

# Main script starts here
echo "Checking system requirements..."
check_python_version
check_git_installation
check_poetry_installation


# Get the top-level directory of the Git repository
REPO_ROOT=$(git rev-parse --show-toplevel)
# Check if the REPO_ROOT was successfully retrieved
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Not a git repository or git command failed."
  exit 1
fi


echo "Enter Snowflake database:"
read DATABASE

echo "Enter Snowflake username:"
read SNOWFLAKE_USERNAME
# Prompt user to enter Snowflake password
echo "Enter Snowflake password:"
read -s PASSWORD

# Replace placeholder in env.example and create .env file
cat << EOF > .envrc
export DAGSTER_HOME=$REPO_ROOT/dagster_project/dagster_home
export SOURCE_BASE_NAME=$SOURCE_BASE_NAME
export DESTINATION__SNOWFLAKE__CREDENTIALS__DATABASE=$DATABASE
export DESTINATION__SNOWFLAKE__CREDENTIALS__HOST="ut63892.north-europe.azure"
export DESTINATION__SNOWFLAKE__CREDENTIALS__USERNAME=$SNOWFLAKE_USERNAME
export DESTINATION__SNOWFLAKE__CREDENTIALS__PASSWORD="$PASSWORD"
EOF

# Securely unset the secret variables
unset PASSWORD

# Install dependencies using poetry
poetry install

# Install pre-commit hook
poetry run pre-commit install --hook-type commit-msg
poetry run pre-commit install

echo "Setup complete!"