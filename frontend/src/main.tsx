import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './index.css';
// 1. IMPORTUJEMY BIBLIOTEKĘ
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// 2. TWORZYMY KLIENTA (SILNIK)
const queryClient = new QueryClient();

const rootElement = document.getElementById('root');
if (rootElement) {
  const root = createRoot(rootElement);
  root.render(
    <React.StrictMode>
      {/* 3. OWIJAMY APLIKACJĘ W PROVIDER */}
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    </React.StrictMode>
  );
}