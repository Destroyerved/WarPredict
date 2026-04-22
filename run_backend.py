#!/usr/bin/env python
import os
import sys
os.chdir(r'c:\Users\vedan\OneDrive\Desktop\WarPredict1')
sys.path.insert(0, r'c:\Users\vedan\OneDrive\Desktop\WarPredict1')

import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.api.main:app", host="0.0.0.0", port=8000, reload=True)
