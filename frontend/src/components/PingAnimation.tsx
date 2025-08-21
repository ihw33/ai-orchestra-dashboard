'use client'

import { useEffect, useState } from 'react'

interface PingAnimationProps {
  cliName: string
  onComplete?: () => void
}

export default function PingAnimation({ cliName, onComplete }: PingAnimationProps) {
  const [visible, setVisible] = useState(true)
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false)
      onComplete?.()
    }, 2000)
    
    return () => clearTimeout(timer)
  }, [onComplete])
  
  if (!visible) return null
  
  return (
    <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
      <div className="relative">
        {/* Ping wave animation */}
        <div className="absolute inset-0 animate-ping">
          <div className="w-20 h-20 bg-green-400 rounded-full opacity-75" />
        </div>
        <div className="relative w-20 h-20 bg-green-500 rounded-full flex items-center justify-center">
          <span className="text-white text-2xl">🏓</span>
        </div>
        <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
          <span className="text-sm font-semibold text-green-600 bg-white px-2 py-1 rounded shadow">
            PING → {cliName.toUpperCase()}
          </span>
        </div>
      </div>
    </div>
  )
}