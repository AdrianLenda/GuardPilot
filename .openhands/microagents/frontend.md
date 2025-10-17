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
- **TypeScript**: Strict mode (no `any`!)
- **Bundler**: Vite
- **Styling**: Tailwind CSS

## 📝 TypeScript Standards
- **Strict mode**: MANDATORY
- **No `any`**: Use `unknown` or `never`
- **Interfaces/Types**: Define types for all data

## ⚛️ React Components
- Functional components only
- Props interface required
- File naming: PascalCase

## 🧪 Testing
- Location: `src/__tests__/`
- Naming: `ComponentName.test.tsx`
- Every component must have a test

## ⚠️ Anti-patterns
- ❌ Don't use `any` type
- ❌ Don't mutate state directly
- ❌ Don't forget dependency array in useEffect