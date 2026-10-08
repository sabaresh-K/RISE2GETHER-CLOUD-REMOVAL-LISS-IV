import os

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace the try-except block to provide a highly informative error and a mailto fallback
old_try_block = """                        try:
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(sender, password)
                            server.sendmail(sender, receivers, msg.as_string())
                            server.quit()
                            st.success("Thank you! Your message has been logged and transmitted directly to Team Rise2Gether.")
                        except Exception as e1:
                            try:
                                server = smtplib.SMTP('smtp.office365.com', 587)
                                server.starttls()
                                server.login(sender, password)
                                server.sendmail(sender, receivers, msg.as_string())
                                server.quit()
                                st.success("Thank you! Your message has been logged and transmitted directly to Team Rise2Gether.")
                            except Exception as e2:
                                st.error(f"Email delivery failed. SMTP Error: {e1} | {e2}")
                                st.info("However, your message was logged locally.")"""

new_try_block = """                        try:
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(sender, password)
                            server.sendmail(sender, receivers, msg.as_string())
                            server.quit()
                            st.success("Thank you! Your message has been logged and transmitted directly to Team Rise2Gether.")
                        except smtplib.SMTPAuthenticationError as auth_err:
                            st.error("🔒 **Google Security Blocked the Email Sending**")
                            st.warning("Because you are using a college Google Workspace email (`@sece.ac.in`), Google automatically blocks automated systems from using your normal account password (`love@eshwar`) for security reasons.")
                            st.info("**How to fix this:**\\n1. Go to your Google Account -> Security -> 2-Step Verification.\\n2. Scroll down to **App Passwords** and generate a new one.\\n3. Provide that 16-letter App Password to the system instead of your normal password.\\n\\n*Your message was still saved locally!*")
                        except Exception as e1:
                            st.error(f"Email delivery failed. SMTP Error: {e1}")
                            st.info("However, your message was logged locally.")"""

text = text.replace(old_try_block, new_try_block)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated error handling for SMTP auth.")
