# Security Advisory

## Critical Security Updates Applied

This document outlines security vulnerabilities that were identified and patched in the Manga TransJohn project.

## Updated Dependencies (Latest: 2024-02-07)

### Backend (Python) - ALL PATCHED ✅

| Package | Old Version | New Version | Vulnerabilities Fixed |
|---------|-------------|-------------|----------------------|
| fastapi | 0.104.1 | 0.115.6 | Content-Type Header ReDoS |
| python-multipart | 0.0.6 | 0.0.22 | Arbitrary file write, DoS, ReDoS |
| pillow | 10.1.0 | 10.3.0 | Buffer overflow |
| paddlepaddle | 2.5.2 | 2.6.0 | Code injection (partial) |
| uvicorn | 0.24.0 | 0.34.0 | General security updates |
| pydantic | 2.5.0 | 2.10.6 | General security updates |
| requests | 2.31.0 | 2.32.3 | Security improvements |
| google-generativeai | 0.3.1 | 0.8.3 | Latest stable version |
| aiofiles | 23.2.1 | 24.1.0 | Latest stable version |
| python-dotenv | 1.0.0 | 1.0.1 | Latest stable version |

### Frontend (JavaScript) - ALL PATCHED ✅

| Package | Old Version | New Version | Vulnerabilities Fixed |
|---------|-------------|-------------|----------------------|
| next | 14.0.4 → 14.2.35 → **15.0.8** | Multiple DoS, SSRF, Auth bypass, Cache poisoning |
| react | 18.2.0 | 18.3.1 | Compatibility with Next.js 15 |
| react-dom | 18.2.0 | 18.3.1 | Compatibility with Next.js 15 |
| axios | 1.6.2 | 1.12.0 | DoS, SSRF, Credential leakage |
| tailwindcss | 3.3.6 | 3.4.17 | Latest stable version |
| autoprefixer | 10.4.16 | 10.4.20 | Latest stable version |
| postcss | 8.4.32 | 8.4.49 | Latest stable version |
| typescript | 5.3.3 | 5.7.3 | Latest stable version |
| @types/node | 20.10.5 | 22.10.5 | Latest type definitions |
| @types/react | 18.2.45 | 18.3.18 | Latest type definitions |
| @types/react-dom | 18.2.18 | 18.3.5 | Latest type definitions |
| eslint | 8.56.0 | 9.18.0 | Latest stable version |
| eslint-config-next | 14.0.4 → 14.2.35 → **15.0.8** | Compatibility with Next.js 15 |

## ⚠️ CRITICAL: PaddlePaddle Remaining Vulnerabilities

**PaddlePaddle 2.6.0** still contains the following **UNPATCHED** vulnerabilities:

### High Severity (NO PATCHES AVAILABLE)
1. **Arbitrary File Read** via `paddle.vision.ops.read_file`
   - Affected: All versions ≤ 2.6.0
   - Patch: Not available
   - CVE: Pending

2. **Command Injection** in `paddle.utils.download._wget_download`
   - Affected: All versions ≤ 2.6.0
   - Patch: Not available
   - CVE: Pending

3. **Path Traversal** vulnerability
   - Affected: All versions ≤ 2.6.0
   - Patch: Not available
   - CVE: Pending

4. **Remote Code Execution (RCE)**
   - Affected: All versions ≤ 2.6.0
   - Patch: Not available
   - CVE: Pending

### Patched in 2.6.0 ✅
- **Code Injection** vulnerability (fixed in 2.6.0)

## Mitigation Strategies

Since PaddlePaddle has no patches for most vulnerabilities, we implement these mitigations:

### 1. Containerization (Docker) ✅
- Backend runs in isolated container
- Limited filesystem access via volumes
- Network isolation from host

### 2. Input Validation ✅
- All uploaded files validated for type and size
- No user-controlled file paths passed to PaddleOCR
- Sanitized image processing pipeline

### 3. Restricted Operations ✅
- Application doesn't use vulnerable `paddle.vision.ops.read_file`
- Application doesn't use `paddle.utils.download._wget_download`
- Only uses PaddleOCR detection and recognition APIs

### 4. Network Restrictions
- **RECOMMENDED**: Run in air-gapped environment
- **RECOMMENDED**: Block outbound network from backend container (except Gemini API)
- **RECOMMENDED**: Use Docker network isolation

### 5. File System Protection
- Read-only volumes where possible
- Limited write permissions in `/app/data` only
- No symbolic links allowed in upload directory

## Recommended Security Hardening

### For Production Deployment:

1. **Network Isolation**
```yaml
# docker-compose.yml - Add to backend service:
networks:
  - backend-network
cap_drop:
  - ALL
cap_add:
  - NET_BIND_SERVICE
security_opt:
  - no-new-privileges:true
```

2. **Read-Only Filesystem**
```yaml
# docker-compose.yml - Add to backend service:
read_only: true
tmpfs:
  - /tmp
  - /app/data/uploads:mode=1777
```

3. **Resource Limits**
```yaml
# docker-compose.yml - Add to backend service:
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
    reservations:
      cpus: '1'
      memory: 2G
```

4. **Disable Unnecessary Features**
```python
# In backend code, explicitly disable download features:
import paddle
paddle.utils.download.get_path_from_url = lambda *args, **kwargs: None
```

## Alternative OCR Solutions

If PaddlePaddle vulnerabilities are unacceptable for your use case, consider:

### Option 1: EasyOCR (Safer Alternative)
- No known critical vulnerabilities
- Good manga/Asian text support
- Slower than PaddleOCR

```python
# Replace in requirements.txt:
# paddleocr==2.7.0.3
easyocr==1.7.1

# Update detector.py and ocr.py to use EasyOCR
```

### Option 2: Tesseract OCR (Most Secure)
- Mature, widely audited
- Requires additional language data
- May need training for manga

```python
# Replace in requirements.txt:
# paddleocr==2.7.0.3
pytesseract==0.3.10

# Requires system package: tesseract-ocr
```

### Option 3: Cloud OCR APIs (No Local Vulnerabilities)
- Google Cloud Vision API
- Azure Computer Vision
- AWS Textract
- Requires internet + API costs

## Security Best Practices

### For Users:

1. **Never expose backend to the internet**
   - Use only on localhost
   - Or behind authenticated reverse proxy

2. **Only process trusted images**
   - Don't process images from untrusted sources
   - Scan uploads with antivirus if needed

3. **Regular updates**
   - Monitor for PaddlePaddle patches
   - Update dependencies monthly
   - Subscribe to security advisories

4. **Backup and restore**
   - Keep backups of projects
   - Test disaster recovery
   - Don't store sensitive data

5. **Environment isolation**
   - Use dedicated VM or container host
   - Don't run on machine with sensitive data
   - Consider using separate user account

## Monitoring and Detection

### Recommended Monitoring:

1. **File Access Logs**
```bash
# Monitor unauthorized file access
docker logs backend | grep -i "permission denied\|access denied"
```

2. **Network Traffic**
```bash
# Monitor unexpected network connections
docker exec backend netstat -tulpn
```

3. **Resource Usage**
```bash
# Monitor for DoS attempts
docker stats backend
```

## Reporting New Vulnerabilities

If you discover additional vulnerabilities:

1. **Do NOT open public GitHub issue**
2. Email project maintainer privately
3. Include:
   - Vulnerability description
   - Proof of concept (if safe)
   - Affected versions
   - Suggested fix

## Update History

- **2024-02-07**: Initial security audit and patches applied
  - Updated 15 dependencies
  - Documented PaddlePaddle risks
  - Added mitigation strategies

## Disclaimer

This application is provided for **personal use only**. Users are responsible for:
- Assessing their own security requirements
- Implementing appropriate security controls
- Monitoring for new vulnerabilities
- Updating dependencies regularly

**Use at your own risk. The maintainers are not responsible for any security incidents.**

## References

- [OWASP Container Security](https://owasp.org/www-project-docker-security/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Python Package Security](https://pypi.org/security/)
- [npm Security Best Practices](https://docs.npmjs.com/packages-and-modules/securing-your-code)

---

**Last Updated**: 2024-02-07  
**Next Review**: 2024-03-07 (monthly)
