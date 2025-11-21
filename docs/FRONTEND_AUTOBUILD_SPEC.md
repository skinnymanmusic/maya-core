# 🏗️ FRONTEND AUTOBUILD SPECIFICATION

**Next.js 14 Build & Deployment Automation**  
**Version:** 1.0  
**Last Updated:** 2025-01-27

---

## 📋 Overview

This document specifies the automated build, test, and deployment pipeline for the MAYA/OMEGA frontend application built with Next.js 14.

---

## 🎯 Build Goals

1. **Fast Builds** - Optimize for speed
2. **Reliable Deployments** - Zero-downtime deployments
3. **Quality Assurance** - Automated testing
4. **Performance** - Optimized bundles
5. **Security** - Dependency scanning

---

## 🏗️ Build Architecture

### Technology Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** TailwindCSS
- **Package Manager:** npm
- **CI/CD:** GitHub Actions
- **Deployment:** Vercel

### Build Process

```
Source Code
    ↓
Lint & Type Check
    ↓
Unit Tests
    ↓
Build (Next.js)
    ↓
Bundle Analysis
    ↓
Deploy (Vercel)
    ↓
Smoke Tests
    ↓
Production
```

---

## 📦 Build Configuration

### package.json Scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "analyze": "ANALYZE=true next build"
  }
}
```

### next.config.js

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  compress: true,
  poweredByHeader: false,
  images: {
    domains: ['your-image-domain.com'],
    formats: ['image/avif', 'image/webp'],
  },
  experimental: {
    optimizeCss: true,
  },
  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
};

module.exports = nextConfig;
```

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

---

## 🔄 GitHub Actions Workflow

### .github/workflows/frontend-ci.yml

```yaml
name: Frontend CI/CD

on:
  push:
    branches: [main, develop]
    paths:
      - 'omega-frontend/**'
      - '.github/workflows/frontend-ci.yml'
  pull_request:
    branches: [main, develop]
    paths:
      - 'omega-frontend/**'

jobs:
  lint-and-typecheck:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: omega-frontend
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: omega-frontend/package-lock.json
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run ESLint
        run: npm run lint
      
      - name: Run TypeScript check
        run: npm run type-check

  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: omega-frontend
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: omega-frontend/package-lock.json
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm run test:coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./omega-frontend/coverage/lcov.info
          flags: frontend

  build:
    runs-on: ubuntu-latest
    needs: [lint-and-typecheck, test]
    defaults:
      run:
        working-directory: omega-frontend
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: omega-frontend/package-lock.json
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build application
        run: npm run build
        env:
          NEXT_PUBLIC_API_URL: ${{ secrets.NEXT_PUBLIC_API_URL }}
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build-files
          path: omega-frontend/.next
          retention-days: 1

  security-scan:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: omega-frontend
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run npm audit
        run: npm audit --audit-level=moderate
      
      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        continue-on-error: true
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  deploy:
    runs-on: ubuntu-latest
    needs: [build, security-scan]
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org: ${{ secrets.VERCEL_ORG }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: omega-frontend
          scope: ${{ secrets.VERCEL_ORG }}
```

---

## 🧪 Testing Strategy

### Unit Tests

**Framework:** Jest + React Testing Library

**Test Files:**
- `*.test.tsx` - Component tests
- `*.test.ts` - Utility tests

**Example:**
```typescript
import { render, screen } from '@testing-library/react';
import { PaymentStatus } from '@/components/payment-status';

describe('PaymentStatus', () => {
  it('displays pending status', () => {
    render(<PaymentStatus status="pending" />);
    expect(screen.getByText('Pending')).toBeInTheDocument();
  });
});
```

### Integration Tests

**Framework:** Playwright

**Test Files:**
- `e2e/*.spec.ts` - End-to-end tests

**Example:**
```typescript
import { test, expect } from '@playwright/test';

test('user can view bookings', async ({ page }) => {
  await page.goto('/bookings');
  await expect(page.locator('h1')).toContainText('Bookings');
});
```

### Coverage Goals

- **Statements:** 80%+
- **Branches:** 75%+
- **Functions:** 80%+
- **Lines:** 80%+

---

## 📊 Build Optimization

### Code Splitting

- Automatic route-based splitting
- Dynamic imports for heavy components
- Lazy load non-critical features

### Image Optimization

- Use Next.js Image component
- AVIF and WebP formats
- Responsive images
- Lazy loading

### Bundle Analysis

```bash
npm run analyze
```

**Tools:**
- `@next/bundle-analyzer`
- Webpack Bundle Analyzer

### Performance Targets

- **First Contentful Paint:** < 1.5s
- **Largest Contentful Paint:** < 2.5s
- **Time to Interactive:** < 3.5s
- **Total Bundle Size:** < 250KB (gzipped)

---

## 🔐 Security

### Dependency Scanning

**Automated:**
- npm audit in CI
- Snyk security scanning
- Dependabot alerts

**Manual:**
- Regular dependency updates
- Review security advisories

### Environment Variables

**Required:**
- `NEXT_PUBLIC_API_URL` - Backend API URL

**Security:**
- Never commit `.env.local`
- Use Vercel environment variables
- Rotate secrets regularly

---

## 🚀 Deployment

### Vercel Configuration

**vercel.json:**
```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm ci",
  "framework": "nextjs",
  "regions": ["iad1"],
  "env": {
    "NEXT_PUBLIC_API_URL": "@api-url"
  }
}
```

### Deployment Process

1. **Push to main** → Triggers workflow
2. **Run tests** → Lint, type-check, unit tests
3. **Build** → Next.js production build
4. **Security scan** → Dependency audit
5. **Deploy** → Vercel deployment
6. **Smoke tests** → Verify deployment
7. **Production** → Live site

### Rollback Strategy

**Vercel:**
- Automatic rollback on build failure
- Manual rollback via dashboard
- Previous deployments available

**Git:**
- Revert commit
- Push to trigger new deployment

---

## 📈 Monitoring

### Build Metrics

- Build duration
- Test execution time
- Bundle size trends
- Deployment frequency

### Performance Monitoring

- Vercel Analytics
- Web Vitals tracking
- Error tracking (Sentry)
- User session replay

---

## 🐛 Troubleshooting

### Build Failures

**Common Issues:**
- Type errors → Fix TypeScript errors
- Lint errors → Fix ESLint warnings
- Test failures → Fix failing tests
- Dependency issues → Update package-lock.json

### Deployment Issues

**Common Issues:**
- Environment variables missing → Check Vercel settings
- Build timeout → Optimize build process
- Memory issues → Increase build memory

---

## ✅ Checklist

Before merging to main:

- [ ] All tests passing
- [ ] No TypeScript errors
- [ ] No ESLint warnings
- [ ] Bundle size acceptable
- [ ] Performance targets met
- [ ] Security scan passed
- [ ] Documentation updated

---

**Version:** 1.0  
**Status:** Active  
**Maintained By:** Frontend Team

