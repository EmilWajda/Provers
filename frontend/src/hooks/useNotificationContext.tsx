import React, { createContext, useContext, useRef, useState, useEffect } from "react";
import type { NotificationData } from "../types";

type NotificationContextValue = {
  data: NotificationData | null;
  showNotification: (data: NotificationData) => void;
};

const NotificationContext = createContext<NotificationContextValue | undefined>(undefined);

export const NotificationProvider: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const [notification, setNotification] = useState<NotificationData | null>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  const showNotification = (data: NotificationData) => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setNotification(data);
    timeoutRef.current = setTimeout(() => setNotification(null), 2000);
  };

  return (
    <NotificationContext.Provider value={{ data: notification, showNotification }}>
      {children}
    </NotificationContext.Provider>
  );
};

export function useNotificationContext(): NotificationContextValue {
  const ctx = useContext(NotificationContext);
  if (!ctx) {
    throw new Error("useNotificationContext must be used within a NotificationProvider");
  }
  return ctx;
}
