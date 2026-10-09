import js from '@eslint/js';
import tseslint from 'typescript-eslint';
export default tseslint.config(
  {ignores: ['node_modules/**', 'renders/**', '.cache/**', 'dist/**', '.venv/**', 'tts/environments/**', 'tts/vendor/**', 'tts/models/**', 'tts/outputs/**', 'tts/.cache/**', 'alignment/environments/**', 'alignment/models/**', 'alignment/outputs/**', 'alignment/.cache/**']},
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {files: ['**/*.{ts,tsx}'], rules: {'@typescript-eslint/no-unused-vars': ['error', {argsIgnorePattern: '^_'}]}},
  {files: ['tts/comparison/app.js'], languageOptions: {globals: {document: 'readonly', fetch: 'readonly', setTimeout: 'readonly', clearTimeout: 'readonly'}}},
  {files: ['**/*.mjs'], languageOptions: {globals: {console: 'readonly', process: 'readonly', Buffer: 'readonly'}}},
);
