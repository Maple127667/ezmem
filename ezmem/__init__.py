from .Memory_main import EasyMemory


__all__ = ["EasyMemory"]

"""
Memory Management Library

This library provides tools for managing and optimizing user memories using AI.

Classes:
    - EasyMemory: Manages user memories and interactions.
    - BaseConfig: Configuration for the memory manager.

Example:
    >>> from Memory import BaseConfig, EasyMemory
    >>> config = BaseConfig(api_key="your-api-key", base_url="https://api.example.com", model="gpt-4")
    >>> memory_manager = EasyMemory(config)
    >>> memory_manager.add("User's memory text", user_id=123)
"""