"use client";

import { useEffect, useState } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { omegaClient, bookingEndpoints } from "@/lib/api/omega-client";
import { PaymentStatus } from "@/components/payment-status";
import { SkeletonCard } from "@/components/skeleton";
import { ErrorMessage } from "@/components/error-message";
import { LoadingSpinner } from "@/components/loading-spinner";

interface Booking {
  booking_id: string;
  service_description: string;
  client_email: string;
  event_date?: string;
  event_location?: string;
  payment_status: string;
  payment_amount?: number;
}

export default function BookingsPage() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchBookings = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await omegaClient.get<Booking[]>(bookingEndpoints.list);
      setBookings(data || []);
    } catch (err: any) {
      console.error("Failed to fetch bookings:", err);
      setError(err.message || "Failed to load bookings. Please check your connection and try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  if (loading && bookings.length === 0) {
    return (
      <AppLayout>
        <div className="container mx-auto p-4 sm:p-6 space-y-6">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold">Bookings</h1>
          <p className="text-sm sm:text-base text-muted-foreground mt-1">
            View and manage your event bookings
          </p>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      </div>
      </AppLayout>
    );
  }

  if (error && bookings.length === 0) {
    return (
      <AppLayout>
        <div className="container mx-auto p-4 sm:p-6">
        <div className="mb-6">
          <h1 className="text-2xl sm:text-3xl font-bold">Bookings</h1>
          <p className="text-sm sm:text-base text-muted-foreground mt-1">
            View and manage your event bookings
          </p>
        </div>
        <ErrorMessage
          title="Unable to load bookings"
          message={error}
          onRetry={fetchBookings}
        />
      </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="container mx-auto p-4 sm:p-6 space-y-4 sm:space-y-6">
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold">Bookings</h1>
        <p className="text-sm sm:text-base text-muted-foreground mt-1">
          View and manage your event bookings
        </p>
      </div>

      {error && (
        <ErrorMessage
          message={error}
          onRetry={fetchBookings}
        />
      )}

      {loading && bookings.length > 0 && (
        <div className="flex items-center justify-center py-4">
          <LoadingSpinner size="sm" />
          <span className="ml-2 text-sm text-muted-foreground">Refreshing...</span>
        </div>
      )}

      {bookings.length === 0 && !loading ? (
        <div className="text-center py-12">
          <p className="text-muted-foreground">No bookings found</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {bookings.map((booking) => (
            <div 
              key={booking.booking_id} 
              className="p-4 border rounded-lg hover:shadow-md transition-shadow touch-manipulation"
            >
              <div className="space-y-2">
                <h3 className="font-semibold text-base sm:text-lg">{booking.service_description}</h3>
                <p className="text-sm text-muted-foreground">
                  {booking.client_email}
                </p>
                {booking.event_date && (
                  <p className="text-sm">
                    📅 {new Date(booking.event_date).toLocaleDateString()}
                  </p>
                )}
                {booking.event_location && (
                  <p className="text-sm text-muted-foreground">
                    📍 {booking.event_location}
                  </p>
                )}
                <div className="mt-3">
                  <PaymentStatus bookingId={booking.booking_id} />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      </div>
    </AppLayout>
  );
}

