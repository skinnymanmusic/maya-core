"use client";

import { useEffect, useState } from "react";
import { omegaClient, stripeEndpoints } from "@/lib/api/omega-client";

interface PaymentStatusProps {
  bookingId: string;
}

interface PaymentStatusData {
  booking_id: string;
  payment_status: "paid" | "pending" | "failed" | "cancelled";
  payment_amount?: number;
  payment_timestamp?: string;
}

export function PaymentStatus({ bookingId }: PaymentStatusProps) {
  const [status, setStatus] = useState<PaymentStatusData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await omegaClient.get<PaymentStatusData>(
          stripeEndpoints.paymentStatus(bookingId)
        );
        setStatus(data);
      } catch (error) {
        console.error("Failed to fetch payment status:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
    
    // Poll every 5 seconds
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, [bookingId]);

  if (loading) {
    return (
      <div className="p-4 border rounded-lg">
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 border-2 border-gray-200 border-t-blue-600 rounded-full animate-spin"></div>
          <span className="text-sm text-muted-foreground">Loading payment status...</span>
        </div>
      </div>
    );
  }
  
  if (!status) {
    return (
      <div className="p-4 border rounded-lg bg-gray-50">
        <p className="text-sm text-muted-foreground">Payment status unavailable</p>
      </div>
    );
  }

  const statusColors: Record<string, string> = {
    paid: "text-green-600",
    pending: "text-yellow-600",
    failed: "text-red-600",
    cancelled: "text-gray-600",
  };

  return (
    <div className="p-3 sm:p-4 border rounded-lg">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-sm sm:text-base">Payment Status</h3>
          <p className="text-xs sm:text-sm text-muted-foreground truncate">
            {status.booking_id}
          </p>
        </div>
        <span className={`px-2 sm:px-3 py-1 sm:py-1.5 rounded text-xs sm:text-sm font-medium min-h-[32px] min-w-[80px] flex items-center justify-center ${statusColors[status.payment_status] || "text-gray-600"}`}>
          {status.payment_status}
        </span>
      </div>
      
      {status.payment_amount && (
        <div className="mt-3 sm:mt-4">
          <p className="text-xl sm:text-2xl font-bold">
            ${status.payment_amount.toFixed(2)}
          </p>
          {status.payment_timestamp && (
            <p className="text-xs sm:text-sm text-muted-foreground mt-1">
              Paid on {new Date(status.payment_timestamp).toLocaleDateString()}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

