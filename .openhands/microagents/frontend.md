---
name: frontend-guidelines
triggers:
  - frontend
  - react
  - typescript
  - component
  - tsx
---

# Frontend Development Guidelines

## 🎨 Tech Stack
- **React**: 18.3+
- **TypeScript**: Strict mode (no \ny\!)
- **Bundler**: Vite
- **Styling**: Tailwind CSS

## 📝 TypeScript Standards
- **Strict mode**: MANDATORY
- **No \ny\**: Use \unknown\ or \
ever\
- **Interfaces/Types**: Define types for all data

## ⚛️ React Components
- Functional components only
- Props interface required
- File naming: PascalCase

## 🧪 Testing
- Location: \src/__tests__/\
- Naming: \ComponentName.test.tsx\
- Every component must have a test

## ⚠️ Anti-patterns
- ❌ Don't use \ny\ type
- ❌ Don't mutate state directly
- ❌ Don't forget dependency array in useEffect
