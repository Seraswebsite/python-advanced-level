class Notification:

    def send_alert(self, message, user=None):
        if user:
            print("Alert for", user, ":", message)
        else:
            print("General Alert:", message)


notification = Notification()

notification.send_alert("The system will restart soon.")

notification.send_alert("You have a new message.", "Samarihi")