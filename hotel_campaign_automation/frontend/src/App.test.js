import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Home Page', () => {
  render(<App />);
  const homeElement = screen.getByText(/Home Page/i);
  expect(homeElement).toBeInTheDocument();
});
