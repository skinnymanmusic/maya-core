/**
 * Error Message Component
 * User-friendly error display with retry option
 */

"use client";

interface ErrorMessageProps {
  title?: string;
  message: string;
  onRetry?: () => void;
  className?: string;
}

export function ErrorMessage({ 
  title = "Something went wrong", 
  message, 
  onRetry,
  className = "" 
}: ErrorMessageProps) {
  return (
    <div className={`p-4 border border-red-200 bg-red-50 rounded-lg ${className}`}>
      <div className="flex items-start space-x-3">
        <div className="flex-shrink-0">
          <svg
            className="w-5 h-5 text-red-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-medium text-red-800">{title}</h3>
          <p className="mt-1 text-sm text-red-700">{message}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-3 text-sm font-medium text-red-600 hover:text-red-800 underline focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 rounded px-2 py-1 min-h-[48px] min-w-[48px]"
            >
              Try again
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

