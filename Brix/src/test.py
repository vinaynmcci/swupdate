from plyer import notification

notification.notify(
    title='Hello',
    message='This is a notification message!',
    app_name='My Application',
    timeout=10,  # Duration the notification should be displayed, in seconds
)
