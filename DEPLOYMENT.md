# Streamlit Cloud Deployment Guide

## Fixed Issues

✅ **ModuleNotFoundError: No module named 'agents.script_agent'**

### Changes Made:

1. **Added proper `__init__.py` files:**
   - `agents/__init__.py` - Exposes all agent functions
   - `utils/__init__.py` - Exposes utility functions

2. **Fixed import structure:**
   - All agent files now use absolute imports
   - Added proper path handling for Streamlit Cloud compatibility
   - Main UI file uses robust import structure

3. **Ensured Streamlit Cloud compatibility:**
   - All imports work with `/mount/src/` root path
   - Proper module structure for Python package recognition

## Deployment Checklist

- [x] `agents/__init__.py` properly exports `generate_initial_script`
- [x] `utils/__init__.py` exports utility functions
- [x] All agent files use absolute imports
- [x] Main UI file has proper path handling
- [x] `requirements.txt` includes all dependencies
- [x] All imports tested and working

## Files Structure

```
s2s-agentic-v1/
├── agents/
│   ├── __init__.py          ✅ Fixed
│   ├── script_agent.py      ✅ Fixed imports
│   ├── prospect_agent.py    ✅ Already correct
│   ├── insight_agent.py     ✅ Already correct
│   ├── finance_agent.py     ✅ Already correct
│   └── engagement_agent.py  ✅ Already correct
├── utils/
│   ├── __init__.py          ✅ Added
│   ├── customer_helper.py   ✅ Already correct
│   └── llm_utils.py         ✅ Already correct
├── script_agent_ui.py       ✅ Fixed imports
├── requirements.txt          ✅ Already correct
└── customer_data.json       ✅ Already present
```

## Environment Variables

Make sure to set these in Streamlit Cloud:
- `OPENAI_API_KEY` - Your OpenAI API key

## Testing

The app has been tested locally and all imports work correctly. The deployment should now work without the `ModuleNotFoundError`. 