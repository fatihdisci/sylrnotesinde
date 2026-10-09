import js from '@eslint/js';
import tseslint from 'typescript-eslint';
export default tseslint.config(
  {ignores: ['node_modules/**', 'renders/**', '.cache/**', 'dist/**', '.venv/**']},
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {files: ['**/*.{ts,tsx}'], rules: {'@typescript-eslint/no-unused-vars': ['error', {argsIgnorePattern: '^_'}]}},
  {files: ['**/*.mjs'], languageOptions: {globals: {console: 'readonly', process: 'readonly', Buffer: 'readonly'}}},
);
