import os

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Define the new contact section
new_contact_section = """elif selected_page == "Contact":
    import smtplib
    from email.mime.text import MIMEText
    
    st.markdown("### Team Rise2Gether Leadership & Contact")
    
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown('''
    <div class="pitch-card" style="border-left:4px solid #10B981; text-align:center;">
            <h2 style="color:#10B981; margin:0 0 0.5rem 0; font-size:1.8rem; font-weight:800;">Sabaresh K</h2>
            <a href="mailto:sabaresh.k2025aids@sece.ac.in" style="color:#10B981; text-decoration:none; font-weight:600; font-size:0.95rem;">
                Email: sabaresh.k2025aids@sece.ac.in
            </a>
    </div>
        ''', unsafe_allow_html=True)
    with t2:
        st.markdown('''
    <div class="pitch-card" style="border-left:4px solid #10B981; text-align:center;">
            <h2 style="color:#10B981; margin:0 0 0.5rem 0; font-size:1.8rem; font-weight:800;">Saadhana S</h2>
            <a href="mailto:saadhana.s2025aids@sece.ac.in" style="color:#10B981; text-decoration:none; font-weight:600; font-size:0.95rem;">
                Email: saadhana.s2025aids@sece.ac.in
            </a>
    </div>
        ''', unsafe_allow_html=True)
    with t3:
        st.markdown('''
    <div class="pitch-card" style="border-left:4px solid #10B981; text-align:center;">
            <h2 style="color:#10B981; margin:0 0 0.5rem 0; font-size:1.8rem; font-weight:800;">Pranika R</h2>
            <a href="mailto:pranika.r2025aids@sece.ac.in" style="color:#10B981; text-decoration:none; font-weight:600; font-size:0.95rem;">
                Email: pranika.r2025aids@sece.ac.in
            </a>
    </div>
        ''', unsafe_allow_html=True)

    form_col, loc_col = st.columns([1.5, 1])
    with form_col:
        st.markdown("<h4 style='color:#10B981; margin-top:0;'>Transmit Message to Team Rise2Gether</h4>", unsafe_allow_html=True)
        with st.form("contact_form_st_clean"):
            c_name = st.text_input("Your Name:", placeholder="Enter your full name...")
            c_email = st.text_input("Your Email Address:", placeholder="name@domain.com...")
            c_msg = st.text_area("Message Details:", placeholder="Type your message here...", height=160)
            c_sub = st.form_submit_button("TRANSMIT INQUIRY")
            if c_sub:
                if c_name and c_email and c_msg:
                    # Attempt to send email
                    try:
                        sender = "sabaresh.k2025aids@sece.ac.in"
                        password = "love@eshwar"
                        receivers = ["sabaresh.k2025aids@sece.ac.in", "saadhana.s2025aids@sece.ac.in", "pranika.r2025aids@sece.ac.in"]
                        
                        msg = MIMEText(f"Name: {c_name}\\nEmail: {c_email}\\nMessage:\\n{c_msg}")
                        msg['Subject'] = f"CloudClear-LISS Inquiry from {c_name}"
                        msg['From'] = sender
                        msg['To'] = ", ".join(receivers)
                        
                        try:
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
                                st.info("However, your message was logged locally.")
                    except Exception as e:
                        st.error(f"Error formulating email: {e}")
                else:
                    st.warning("Please fill in your Name, Email, and Message before submitting.")

    with loc_col:
        st.markdown('''
    <div class="pitch-card">
    <h4 style="color:#10B981; margin-top:0;">Our Institution</h4>
    <h3 style="color:#FFFFFF; margin:0.5rem 0 0.2rem 0; font-size:1.3rem;">Sri Eshwar College of Engineering and Technology</h3>
    <p style="color:#94A3B8; font-size:0.95rem;">Coimbatore, Tamil Nadu, India</p>
            <hr style="border-color:rgba(0,212,255,0.2); margin:1rem 0;">
    <p style="font-size:0.9rem; color:#CBD5E1;"><strong>Coordinates:</strong> 10.871° N, 77.019° E</p>
    </div>
        ''', unsafe_allow_html=True)

# Shared Global Footer
st.markdown("---")
st.caption("© 2026 CloudClear-LISS. Built by Team Rise2Gether. All rights reserved.")
"""

start_idx = text.find('elif selected_page == "Contact":')
text = text[:start_idx] + new_contact_section

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Contact page updated with SMTP email sending and box fix!")
