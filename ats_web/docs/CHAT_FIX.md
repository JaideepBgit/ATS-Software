# Fix for Chat "404 Not Found" Error

## Problem
Getting `404 Not Found` error when trying to ask questions in the chat interface.

## Root Cause
The backend server needs to be restarted after code changes. The `/api/ask` endpoint exists in the code but the running server doesn't have it loaded.

## Solution

### Option 1: Restart Backend (Recommended)

1. **Stop the backend server**
   - Press `Ctrl+C` in the terminal where the backend is running

2. **Start it again**
   ```bash
   cd ats_web/backend
   python main.py
   ```

3. **Verify it's working**
   - You should see: `INFO:     Application startup complete.`
   - Try asking a question in the chat

### Option 2: Check for Import Errors

If restarting doesn't work, there might be an import error:

1. **Test the imports**
   ```bash
   cd ats_web/backend
   python test_endpoints.py
   ```

2. **Look for errors**
   - If you see import errors about `chromadb`, `faiss`, or `sentence_transformers`
   - Install missing dependencies:
   ```bash
   pip install chromadb faiss-cpu sentence-transformers numpy
   ```

3. **Restart backend again**
   ```bash
   python main.py
   ```

### Option 3: Verify Endpoint Registration

Check if the endpoint is registered:

```bash
curl http://localhost:8000/docs
```

This opens the FastAPI automatic documentation. Look for `/api/ask` in the list.

## Quick Test

After restarting, test the endpoint directly:

```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": "test_123",
    "question": "test"
  }'
```

Expected response (even if candidate doesn't exist):
```json
{"detail": "Candidate not found"}
```

If you get this, the endpoint is working! The 404 is gone.

## Common Issues

### Issue: "Module not found" errors
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Backend won't start
**Solution**: Check for syntax errors
```bash
python -m py_compile main.py
```

### Issue: Port already in use
**Solution**: Kill the old process
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Then restart
python main.py
```

### Issue: Still getting 404
**Solution**: Check the frontend is calling the right URL
- Open browser DevTools (F12)
- Go to Network tab
- Try asking a question
- Check the request URL - should be `http://localhost:8000/api/ask`

## Verification Checklist

- [ ] Backend server restarted
- [ ] No import errors in console
- [ ] Can access http://localhost:8000/docs
- [ ] `/api/ask` appears in the docs
- [ ] Frontend is running on http://localhost:3000
- [ ] Browser console shows no CORS errors

## Still Not Working?

If the issue persists:

1. **Check backend console** for error messages
2. **Check browser console** (F12) for frontend errors
3. **Verify the request** in Network tab:
   - URL should be: `http://localhost:8000/api/ask`
   - Method should be: `POST`
   - Content-Type should be: `application/json`

## Prevention

To avoid this in the future:
- Always restart the backend after code changes
- Use a development server with auto-reload:
  ```bash
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```

The `--reload` flag automatically restarts when code changes!
