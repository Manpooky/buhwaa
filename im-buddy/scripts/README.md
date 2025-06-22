# Scripts Directory

This directory contains utility scripts for the im-buddy project. The scripts are organized into core utility modules and simple wrapper scripts.

## Core Utility Modules

### `env_utils.py`

Utilities for managing environment variables and .env files.

- `load_env_file()`: Load environment variables from .env file
- `save_env_file()`: Save environment variables to .env file
- `update_env_var()`: Update an environment variable
- `setup_llama_api_key()`: Set up the Llama API key
- `setup_supabase_credentials()`: Set up Supabase credentials
- `setup_all_credentials()`: Set up all required credentials
- `check_environment()`: Check if all required environment variables are set

### `supabase_utils.py`

Utilities for Supabase operations.

- `get_supabase_credentials()`: Get Supabase credentials
- `test_supabase_connection()`: Test connection to Supabase
- `check_bucket_exists()`: Check if a bucket exists
- `create_bucket()`: Create a bucket
- `test_storage_operations()`: Test storage operations
- `setup_supabase()`: Complete Supabase setup

### `llama_utils.py`

Utilities for testing and interacting with the Meta Llama API.

- `get_llama_api_key()`: Get the Llama API key
- `chat_with_llama()`: Chat with Llama API
- `test_translation()`: Test translation service
- `test_tips_generation()`: Test tips generation service
- `interactive_chat()`: Interactive chat session
- `test_all_services()`: Test all Llama API services

## Wrapper Scripts

### Environment Setup

- `setup_env.py`: Set up environment variables
- `check_env.py`: Check environment variables

### Supabase Testing

- `test_supabase.py`: Test Supabase connection
- `setup_supabase.py`: Set up Supabase storage

### Llama API Testing

- `test_llama.py`: Test Llama API services
- `chat.py`: Interactive chat with Llama API

## Usage

To set up your environment:

```bash
python scripts/setup_env.py
```

To check your environment:

```bash
python scripts/check_env.py
```

To set up Supabase:

```bash
python scripts/setup_supabase.py
```

To test Supabase connection:

```bash
python scripts/test_supabase.py
```

To test Llama API:

```bash
python scripts/test_llama.py
```

To chat with Llama API:

```bash
python scripts/chat.py
``` 