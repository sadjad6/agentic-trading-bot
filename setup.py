from setuptools import find_packages,setup

setup(name="agentic-trading-system",
       version="0.0.1",
       
       packages=find_packages(),
       install_requires=['lancedb','langchain','langgraph','tavily-python','polygon']
       )