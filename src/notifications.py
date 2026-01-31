import datetime

class NotificationManager:
    def send_notification(self, message, level="info"):
        """
        Mock notification sender.
        In a real app, this would send SMS or Email.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level.upper()}] {message}"
        
        # Simulate sending
        print(f"📧 SENDING NOTIFICATION: {message}")
        
        # Log to file
        with open("emergency_logs.txt", "a") as f:
            f.write(log_entry + "\n")
            
        return log_entry
