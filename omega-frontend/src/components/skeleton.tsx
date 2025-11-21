/**
 * Skeleton Loading Components
 * For perceived performance on mobile
 */

export function SkeletonCard() {
  return (
    <div className="p-4 border rounded-lg animate-pulse">
      <div className="space-y-3">
        <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        <div className="h-3 bg-gray-200 rounded w-1/2"></div>
        <div className="h-3 bg-gray-200 rounded w-2/3"></div>
        <div className="h-20 bg-gray-200 rounded"></div>
      </div>
    </div>
  );
}

export function SkeletonText({ width = "w-full" }: { width?: string }) {
  return (
    <div className={`h-4 bg-gray-200 rounded animate-pulse ${width}`}></div>
  );
}

export function SkeletonBadge() {
  return (
    <div className="h-6 w-20 bg-gray-200 rounded animate-pulse"></div>
  );
}

