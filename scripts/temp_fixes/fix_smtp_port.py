import os
path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace the try block to try SMTP_SSL on 465
old_block = """                        try:
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(sender, password)
                            server.sendmail(sender, receivers, msg.as_string())
                            server.quit()
                            st.success("Thank you! Your message has been logged and transmitted directly to Team Rise2Gether.")
                        except smtplib.SMTPAuthenticationError as auth_err:"""

new_block = """                        try:
                            # Try Port 465 (SSL) first as Port 587 is often blocked by college Wi-Fi/ISPs
                            server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=5)
                            server.login(sender, password)
                            server.sendmail(sender, receivers, msg.as_string())
                            server.quit()
                            st.success("Thank you! Your message has been logged and transmitted directly to Team Rise2Gether.")
                        except smtplib.SMTPAuthenticationError as auth_err:"""

text = text.replace(old_block, new_block)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated SMTP to use Port 465 SSL to bypass ISP blocks")
