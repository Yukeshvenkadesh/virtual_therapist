import type { Metadata } from 'next'
import { BrowserRouter } from 'react-router-dom'
import './globals.css'

export const metadata: Metadata = {
  title: 'Virtual Therapist',
  description: 'AI-powered mental health analysis tool',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>
        <BrowserRouter>
          {children}
        </BrowserRouter>
      </body>
    </html>
  )
}
