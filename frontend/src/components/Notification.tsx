import { useNotificationContext } from "../hooks/useNotificationContext";

export default function Notification() {
  const notification = useNotificationContext().data;

  if (!notification) {
    return null;
  }

  return (
    <div
      className={`fixed top-6 left-1/2 -translate-x-1/2 px-6 py-3 rounded-lg shadow-xl text-white font-medium ${
        notification.type === "success" ? "bg-green-600" : "bg-red-600"
      } z-50 transition-all animate-fade-in`}
    >
      {notification.message}
    </div>
  );
}
