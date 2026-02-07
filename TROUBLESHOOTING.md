# Troubleshooting Guide

## Common Issues and Solutions

### Backend Issues

#### 1. "GEMINI_API_KEY not set"

**Problem**: The backend can't find your Gemini API key.

**Solutions**:
```bash
# Check if .env file exists
ls -la .env

# Check if key is set
cat .env | grep GEMINI_API_KEY

# If missing, create .env from example
cp .env.example .env

# Edit .env and add your key
nano .env  # or use your preferred editor
```

#### 2. PaddleOCR Initialization Fails

**Problem**: Not enough memory or missing dependencies.

**Solutions**:
- Increase Docker memory limit to at least 4GB
- Check Docker logs: `docker-compose logs backend`
- Rebuild containers: `docker-compose down && docker-compose up --build`

#### 3. "Failed to load image"

**Problem**: Invalid image format or corrupted file.

**Solutions**:
- Ensure image is PNG, JPG, or JPEG
- Check file size (should be under 10MB)
- Try converting image: `convert input.jpg output.png`

#### 4. Translation Takes Too Long

**Problem**: Gemini API rate limits or network issues.

**Solutions**:
- Check Gemini API quotas
- Reduce number of regions
- Enable cover mode to filter large text
- Check network connectivity

### Frontend Issues

#### 1. "Cannot connect to backend"

**Problem**: Backend not running or wrong URL.

**Solutions**:
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check Docker containers
docker-compose ps

# Restart services
docker-compose restart
```

#### 2. Upload Button Not Working

**Problem**: File input issues or CORS error.

**Solutions**:
- Check browser console for errors (F12)
- Verify backend CORS settings
- Try different browser
- Clear browser cache

#### 3. Canvas Not Displaying

**Problem**: Image loading issue or browser compatibility.

**Solutions**:
- Check browser console for errors
- Ensure browser supports HTML5 Canvas
- Try Chrome or Firefox
- Disable browser extensions

#### 4. Translations Not Saving

**Problem**: API communication issue.

**Solutions**:
- Check network tab in browser dev tools
- Verify backend is responding: `curl http://localhost:8000/health`
- Check backend logs: `docker-compose logs backend`

### Docker Issues

#### 1. "Cannot start service"

**Problem**: Port already in use or Docker daemon issue.

**Solutions**:
```bash
# Check if ports are in use
lsof -i :3000
lsof -i :8000

# Kill process using the port
kill -9 <PID>

# Or change ports in docker-compose.yml
# Edit ports: - "3001:3000" and - "8001:8000"
```

#### 2. "Build failed"

**Problem**: Dependency installation issue.

**Solutions**:
```bash
# Clean Docker build cache
docker-compose down
docker system prune -a

# Rebuild from scratch
docker-compose up --build --force-recreate
```

#### 3. Volume Permission Issues

**Problem**: Can't write to mounted volumes.

**Solutions**:
```bash
# Fix permissions
sudo chown -R $USER:$USER ./data
chmod -R 755 ./data

# Or run Docker with user namespace
docker-compose down
docker-compose up --user $(id -u):$(id -g)
```

### Performance Issues

#### 1. Slow Processing

**Causes and Solutions**:

- **Large Images**: Resize images to max 2000x2000 before uploading
- **Too Many Regions**: Enable cover mode or manually ignore regions
- **Low Memory**: Increase Docker memory allocation
- **Slow Network**: Check internet speed (Gemini API requires good connection)

#### 2. High Memory Usage

**Solutions**:
```bash
# Monitor memory
docker stats

# Limit backend memory
# Add to docker-compose.yml under backend:
deploy:
  resources:
    limits:
      memory: 4G
```

### API Errors

#### 1. 429 Rate Limit Exceeded

**Problem**: Too many requests to Gemini API.

**Solutions**:
- Wait 1 minute and try again
- Reduce translation batch size
- Check Gemini API quotas

#### 2. 500 Internal Server Error

**Problem**: Backend crash or unhandled exception.

**Solutions**:
- Check backend logs: `docker-compose logs backend`
- Look for Python stack traces
- Restart backend: `docker-compose restart backend`

#### 3. 413 Payload Too Large

**Problem**: Image file too large.

**Solutions**:
- Compress image before uploading
- Resize to reasonable dimensions
- Maximum recommended: 5MB, 2000x2000px

### Font Issues

#### 1. "Font not found" Warning

**Problem**: WildWorlds font not in backend/fonts/.

**Solutions**:
```bash
# Check if font exists
ls -la backend/fonts/WildWorlds.ttf

# Copy font to correct location
cp /path/to/WildWorlds.ttf backend/fonts/

# Restart backend
docker-compose restart backend
```

**Note**: App works with default font if WildWorlds is missing.

### Data Issues

#### 1. Projects Not Saving

**Problem**: Permission or disk space issue.

**Solutions**:
```bash
# Check disk space
df -h

# Check data directory permissions
ls -la data/

# Fix permissions
chmod -R 755 data/
```

#### 2. Can't Find Exported Files

**Problem**: Files saved to unexpected location.

**Solutions**:
- Check browser download folder
- For Docker: Files in `./data/output/`
- Check browser download settings

## Getting Help

If issues persist:

1. **Check Logs**:
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```

2. **Enable Debug Mode**:
   - Backend: Set `LOG_LEVEL=DEBUG` in .env
   - Frontend: Check browser console (F12)

3. **Verify Setup**:
   ```bash
   ./start.sh  # Use the startup script
   ```

4. **Report Issue**:
   - Open GitHub issue
   - Include: OS, Docker version, error logs, steps to reproduce

## Useful Commands

```bash
# View all logs
docker-compose logs -f

# Restart everything
docker-compose restart

# Stop everything
docker-compose down

# Rebuild everything
docker-compose up --build --force-recreate

# Check service health
curl http://localhost:8000/health
curl http://localhost:3000

# Clean everything (WARNING: deletes data)
docker-compose down -v
rm -rf data/*
```
