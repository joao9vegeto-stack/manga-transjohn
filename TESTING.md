# Testing Guide

This guide provides step-by-step instructions for testing Manga TransJohn.

## Prerequisites

1. Docker and Docker Compose installed
2. GEMINI_API_KEY set in `.env` file
3. (Optional) WildWorlds.ttf font in `backend/fonts/`
4. Test manga images ready

## Quick Test

### 1. Start the Application

```bash
# Using the convenience script
./start.sh

# Or manually
docker-compose up --build
```

Wait for both services to be healthy:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs

### 2. Basic Translation Test

1. Open http://localhost:3000
2. Upload a manga page (drag-and-drop or click)
3. Select source language (e.g., "Japanese")
4. Click "Translate"
5. Wait for processing (10-30 seconds)
6. Verify:
   - All text regions detected
   - OCR extracted text correctly
   - Translations in Brazilian Portuguese
   - Text rendered on image

### 3. Editor Test

In the editor:
1. Click on different regions
2. Edit a translation
3. Click "Save Changes"
4. Toggle "Show Translation" checkbox
5. Use Undo/Redo buttons
6. Click "Export Image"

## Comprehensive Tests

### Test 1: Simple Dialogue Page

**Objective**: Verify basic translation pipeline.

**Steps**:
1. Upload a manga page with 3-5 speech bubbles
2. Select source language: Japanese
3. Cover mode: OFF
4. Translate

**Expected Results**:
- ✅ All speech bubbles detected
- ✅ Text extracted correctly
- ✅ Natural Portuguese translations
- ✅ Text fits in bubbles
- ✅ White text with black outline
- ✅ No artifacts from inpainting

### Test 2: Cover Page Translation

**Objective**: Test cover mode functionality.

**Steps**:
1. Upload a manga cover with large title
2. Select source language: Japanese
3. Cover mode: ON
4. Translate

**Expected Results**:
- ✅ Large title NOT translated (or filtered)
- ✅ Smaller text (subtitles) translated
- ✅ Can manually ignore title region
- ✅ Can delete title translation

**Manual Steps**:
1. If title was translated, select its region
2. Click "Ignore Region"
3. Click "Re-run Translation"
4. Verify title is now ignored

### Test 3: Region Editing

**Objective**: Test interactive editing features.

**Steps**:
1. Complete a translation
2. Select a region in the list
3. Edit the translated text
4. Save changes
5. Toggle visibility off/on
6. Use Undo
7. Use Redo
8. Delete the region

**Expected Results**:
- ✅ Edits persist
- ✅ Visibility toggles work
- ✅ Undo restores previous state
- ✅ Redo restores undone state
- ✅ Delete removes translation

### Test 4: Multiple Languages

**Objective**: Test different source languages.

**Test Cases**:
1. Japanese manga → pt-BR
2. Korean manhwa → pt-BR
3. Chinese manhua → pt-BR
4. English comic → pt-BR

**Expected Results**:
- ✅ OCR works for each language
- ✅ Translations are natural
- ✅ Honorifics handled appropriately

### Test 5: Edge Cases

**Objective**: Test error handling and edge cases.

**Test Cases**:

1. **Very Small Text**
   - Upload image with tiny text
   - Verify: Some regions might be missed (acceptable)

2. **Sound Effects**
   - Upload page with onomatopoeia
   - Verify: Translated to pt-BR equivalents or kept with note

3. **Rotated Text**
   - Upload page with angled/rotated text
   - Verify: Detection handles various orientations

4. **Dense Page**
   - Upload page with 15+ text regions
   - Verify: All regions processed, acceptable performance

5. **Large Image**
   - Upload 4000x6000px image
   - Verify: Handles large images, may be slow

### Test 6: Export Functionality

**Objective**: Test export features.

**Steps**:
1. Complete a translation
2. Click "Export Image"
3. Verify downloaded PNG
4. Click "Export Project JSON"
5. Verify JSON file

**Expected Results**:
- ✅ PNG image downloads
- ✅ Image contains translations
- ✅ JSON file contains project data
- ✅ JSON includes all regions and translations

### Test 7: Re-run Translation

**Objective**: Test re-processing with changes.

**Steps**:
1. Complete a translation
2. Mark 2 regions as "Ignore"
3. Delete 1 region
4. Edit 1 translation
5. Click "Re-run Translation"

**Expected Results**:
- ✅ Ignored regions not re-translated
- ✅ Deleted region stays deleted
- ✅ Edited region keeps edit
- ✅ Other regions re-translated

## API Testing

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "services": {
    "detector": true,
    "ocr": true,
    "translator": true,
    "inpainter": true,
    "typesetter": true
  }
}
```

### Upload Test

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@test-images/sample.png"
```

Expected response:
```json
{
  "image_id": "uuid-here",
  "filename": "sample.png",
  "path": "/app/data/uploads/uuid-here.png"
}
```

### Full API Documentation

Visit: http://localhost:8000/docs

## Performance Benchmarks

### Expected Performance

| Operation | Time (typical) | Time (acceptable) |
|-----------|---------------|-------------------|
| Upload | < 1s | < 3s |
| Detection | 1-3s | < 5s |
| OCR (5 regions) | 2-5s | < 10s |
| Translation (5 texts) | 5-10s | < 20s |
| Inpainting | 2-5s | < 10s |
| Typesetting | < 1s | < 2s |
| **Total Pipeline** | **10-20s** | **< 40s** |

### Performance Test

1. Note start time
2. Upload and translate a page with 5-10 regions
3. Note completion time
4. Compare with benchmarks above

## Troubleshooting Tests

If tests fail, check:

1. **Logs**:
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```

2. **Services Running**:
   ```bash
   docker-compose ps
   ```

3. **API Key**:
   ```bash
   docker-compose exec backend env | grep GEMINI
   ```

4. **Disk Space**:
   ```bash
   df -h
   ```

## Regression Testing

After making changes:

1. Run all tests above
2. Check for new errors
3. Verify performance hasn't degraded
4. Test edge cases

## Reporting Issues

When reporting test failures:

1. Which test failed
2. Expected vs actual result
3. Screenshots if applicable
4. Backend/frontend logs
5. Environment details (OS, Docker version)

## Automated Testing

(Future improvement)

Consider adding:
- Unit tests for backend services
- Integration tests for API endpoints
- E2E tests for frontend
- Visual regression tests
- Performance benchmarks

## Test Checklist

Before release:

- [ ] Basic translation works
- [ ] All 7 languages supported
- [ ] Cover mode filters large text
- [ ] Editor allows edits
- [ ] Undo/Redo works
- [ ] Export PNG works
- [ ] Export JSON works
- [ ] Re-run preserves edits
- [ ] Docker deployment works
- [ ] Documentation is accurate
- [ ] No security issues
- [ ] Performance acceptable
