import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

import { AuthProvider } from '@asgardeo/auth-react';
import { authConfig } from "./config/authConfig.ts"

ReactDOM.createRoot(document.getElementById('root')!).render(
  <AuthProvider config={authConfig}>
    <React.StrictMode>
      <App />
    </React.StrictMode>
  </AuthProvider>
)