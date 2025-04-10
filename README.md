# On Running MCP

A Model-Context-Protocol (MCP) server for interacting with the On Running website API.

## Overview

This project provides an interface to the On Running website's product data through a FastMCP server. It allows you to:

- Query the On Running API with various filters
- Get product information including names, images, and activities
- Filter products by type, subtype, and gender

## Installation

Requires Python 3.12+

```bash
# Clone the repository
git clone https://github.com/yourusername/on-running-mcp.git
cd on-running-mcp

# Create and activate a virtual environment (optional but recommended)
uv venv

# Sync the dependencies
uv sync
```

## Usage

### Add the Server Config to Claude Desktop.

```bash
cd on_running_mcp
uv run mcp install server.py
```

### Available Tools

The MCP server provides the following tools:

- `make_query`: Make a query to the On Running API with optional filters
- `get_product_names`: Get all product names from the results
- `get_activities`: Get activities associated with each product
- `filter_by_product_name`: Find a specific product by name
- `get_product_image`: Get an image for a specific product
- `get_product_type_options`: List available product types (shoes, apparel, accessories)
- `get_product_subtype_options`: List available product subtypes (tops, shorts, etc.)
- `get_gender_options`: List available gender options (men's, women's, kids)

### Example Usage

> I am running a marathon later this month, can you help me to find a pair of socks for running in?

## Project Structure

- `on_running_mcp/`: Main package directory
  - `server.py`: MCP server implementation with tool definitions
  - `core/`: Core API implementation
    - `api.py`: On Running API client
    - `schemas.py`: Pydantic models for API data

