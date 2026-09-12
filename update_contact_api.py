import os

path = r"c:\Users\sabar\Downloads\CLOUD REMOVAL\src\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

start_str = '    with form_col:\n        st.markdown("<h4 style=\'color:#10B981; margin-top:0;\'>Transmit Message to Team Rise2Gether</h4>", unsafe_allow_html=True)'
end_str = '                else:\n                    st.warning("Please fill in your Name, Email, and Message before submitting.")\n\n'

start_idx = text.find(start_str)
end_idx = text.find(end_str) + len(end_str)

new_form = """    with form_col:
        html_code = '''
        <div style="font-family: sans-serif; color: #E2E8F0;">
            <h4 style="color:#10B981; margin-top:0; font-size:1.1rem; margin-bottom:1rem;">Transmit Message to Team Rise2Gether</h4>
            <form id="contactForm" style="display:flex; flex-direction:column; gap:15px;">
                <div>
                    <label style="font-size:0.9rem; font-weight:600; margin-bottom:5px; display:block;">Your Name:</label>
                    <input type="text" id="name" required placeholder="Enter your full name..." style="width:100%; box-sizing:border-box; padding:0.8rem; background:rgba(4,30,22,0.9); border:1px solid #10B981; color:#fff; border-radius:8px; outline:none; font-family:sans-serif;">
                </div>
                <div>
                    <label style="font-size:0.9rem; font-weight:600; margin-bottom:5px; display:block;">Your Email Address:</label>
                    <input type="email" id="email" required placeholder="name@domain.com..." style="width:100%; box-sizing:border-box; padding:0.8rem; background:rgba(4,30,22,0.9); border:1px solid #10B981; color:#fff; border-radius:8px; outline:none; font-family:sans-serif;">
                </div>
                <div>
                    <label style="font-size:0.9rem; font-weight:600; margin-bottom:5px; display:block;">Message Details:</label>
                    <textarea id="msg" required placeholder="Type your message here..." style="width:100%; box-sizing:border-box; padding:0.8rem; background:rgba(4,30,22,0.9); border:1px solid #10B981; color:#fff; border-radius:8px; outline:none; font-family:sans-serif;" rows="6"></textarea>
                </div>
                <button type="submit" style="padding:0.8rem; background:linear-gradient(90deg, #047857 0%, #10B981 100%); color:white; border:1px solid #34D399; border-radius:8px; cursor:pointer; font-weight:800; text-transform:uppercase; transition:0.3s;">TRANSMIT INQUIRY</button>
            </form>
            <div id="statusMsg" style="margin-top:15px; padding:10px; border-radius:5px; display:none; font-weight:bold; font-size:0.9rem;"></div>
        </div>

        <script>
        document.getElementById('contactForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const msg = document.getElementById('msg').value;
            const status = document.getElementById('statusMsg');
            
            status.style.display = 'block';
            status.style.background = 'rgba(16, 185, 129, 0.2)';
            status.style.color = '#10B981';
            status.innerText = "Transmitting to Team Rise2Gether via FormSubmit API...";
            
            const payload = {
                name: name,
                email: email,
                message: msg,
                _subject: "CloudClear-LISS Inquiry from " + name
            };
            
            // Primary Route: FormSubmit AJAX in Parallel
            const emails = ["sabaresh.k2025aids@sece.ac.in", "saadhana.s2025aids@sece.ac.in", "pranika.r2025aids@sece.ac.in"];
            const promises = emails.map(recipient => {
                return fetch("https://formsubmit.co/ajax/" + recipient, {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });
            });
            
            Promise.all(promises).then(responses => {
                status.style.background = 'rgba(16, 185, 129, 0.2)';
                status.style.color = '#10B981';
                status.innerText = "Thank you! Your message has been safely transmitted to Team Rise2Gether.";
                document.getElementById('contactForm').reset();
            }).catch(err => {
                // Fallback Route: Native Mailto
                status.style.background = 'rgba(239, 68, 68, 0.2)';
                status.style.color = '#EF4444';
                status.innerText = "API blocked. Launching default email client (Mailto) fallback...";
                window.top.location.href = `mailto:sabaresh.k2025aids@sece.ac.in?subject=CloudClear-LISS Inquiry&body=Name: ${name}%0AEmail: ${email}%0AMessage:%0A${msg}`;
            });
        });
        </script>
        '''
        import streamlit.components.v1 as components
        components.html(html_code, height=520, scrolling=False)

"""

text = text[:start_idx] + new_form + text[end_idx:]

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Injected AJAX custom FormSubmit logic")
