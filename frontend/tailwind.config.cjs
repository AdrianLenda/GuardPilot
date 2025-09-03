/**
 * Tailwind CSS configuration for GuardPilot frontend.
 * Defines a dark mode palette and scans the project files for class usage.
 */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}'
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#5D5FEF',
        },
      },
      maxWidth: {
        '68ch': '68ch',
      },
    },
  },
  plugins: [],
};
