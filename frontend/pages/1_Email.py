import streamlit as st
import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime, parseaddr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit.components.v1 as components
import html
import re
import time

################################
# SESSION CREDENTIALS
# Initialize session state for login status and credentials
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_password" not in st.session_state:
    st.session_state.user_password = ""
if "current_page" not in st.session_state:
    st.session_state.current_page = "email_list"
if "selected_email" not in st.session_state:
    st.session_state.selected_email = None

# dummy variable for rerun
# st.experimental_rerun()  WONT WORK AFTER STREAMLIT UPDATES !!
# st.experimental_set_query_params WILL STOP WORKING EITHER !!
# best approach : using st.sesstion_state with a temporary variable
if "trigger_rerun" not in st.session_state:  # Dummy variable for rerun
    st.session_state.trigger_rerun = False

#####################
# CSS for email cards
css_style = """
<style>
* { color: #fff; }
.email-card {
    border: 1px solid rgba(255, 255, 255, 0.18);
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 15px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    color: #fff;
}
.email-card h3 { font-size: 1.4em; }
.email-card .email-date { font-size: 0.9em; color: #ccc; }
.divider { border: none; border-top: 1px solid rgba(255, 255, 255, 0.2); margin: 20px 0; }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

#######################
# UTILITY FUNCTIONS
#######################
def decode_mime_header(value):
    decoded = decode_header(value)
    subject, encoding = decoded[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or 'utf-8')
    return subject

def get_body_from_message(msg):
    body = None
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if "attachment" not in content_disposition:
                if content_type == "text/html":
                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    return body
                elif content_type == "text/plain" and body is None:
                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
    else:
        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
    return body or ""

def fetch_emails(username, password, imap_url='imap.gmail.com', search_criteria="ALL", email_limit=10):
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(username, password)
        mail.select("inbox")
        result, data = mail.search(None, search_criteria)
        email_ids = data[0].split()

        emails = []
        for email_id in email_ids[-email_limit:]:
            result, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_mime_header(msg["Subject"])
                    raw_author = msg.get("From")
                    author_name, author_email = parseaddr(raw_author)
                    author_name = decode_mime_header(author_name)
                    date_ = msg.get("Date")
                    date_obj = parsedate_to_datetime(date_)
                    body = get_body_from_message(msg)

                    emails.append({
                        "id": email_id.decode('utf-8'),
                        "author_name": html.escape(author_name),
                        "author_email": html.escape(author_email),
                        "subject": html.escape(subject),
                        "date": date_obj,
                        "body": body,
                    })
        emails.reverse() # SHOW THE NEWS EMAIL ON TOP !
        mail.logout()
        return emails
    except imaplib.IMAP4.error as e:
        st.error("Authentication failed. Please check your email and app password.")
        st.session_state.logged_in = False
        return []

def send_reply(username, password, recipient_email, subject, reply_body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    try:
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(reply_body, 'plain'))
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.sendmail(username, recipient_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send reply: {e}")
        return False

#####################
# STREAMLIT INTERFACE
#####################
# Login and Email Display Logic
if not st.session_state.logged_in:
    st.title("Login to Email Application")
    user_email = st.text_input("Email", placeholder="Enter your email")
    user_password = st.text_input("App Password", placeholder="Enter your app-specific password", type="password")
    st.warning("Please log in to access your emails.")
    if st.button("Login"):
        st.session_state.user_email = user_email
        st.session_state.user_password = user_password
        emails = fetch_emails(user_email, user_password)
        if emails:
            st.session_state.logged_in = True
            st.session_state.current_page = "email_list"
            st.success("Login successful!")
            time.sleep(0.5)  # Wait 1 second before the next refresh
            st.session_state.trigger_rerun = not st.session_state.trigger_rerun  # Toggle dummy variable to force rerun

else:
    # Email Dashboard after Login
    if st.session_state.current_page == "email_list":
        st.title("Emails Received")
        emails = fetch_emails(st.session_state.user_email, st.session_state.user_password)
        if emails:
            st.write(f"Showing {len(emails)} emails:")
            for email_info in emails:
                email_id_str = email_info['id']
                is_read = st.session_state.get(f'read_status_{email_id_str}', False)
                st.markdown(f"""
                <div class="email-card">
                    <h3>{email_info['subject']}</h3>
                    <p><strong>From:</strong> {email_info['author_name']} &lt;{email_info['author_email']}&gt;</p>
                    <p class="email-date"><strong>Date:</strong> {email_info['date'].strftime('%Y-%m-%d %H:%M:%S')}</p>
                """, unsafe_allow_html=True)

                with st.expander("Show Email Content"):
                    components.html(f"<div style='color: white;'>{email_info['body']}</div>", height=300, scrolling=True)

                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.checkbox(f"Mark as Read", key=email_info['id'], value=is_read):
                        mark_email_as_read(st.session_state.user_email, st.session_state.user_password, email_info['id'])
                        st.session_state[f'read_status_{email_id_str}'] = True
                    else:
                        st.session_state[f'read_status_{email_id_str}'] = False
                with col2:
                    if st.button("Answer", key=f"answer_{email_info['id']}"):
                        st.session_state.selected_email = email_info
                        st.session_state.current_page = "answer_page"
                        st.session_state.trigger_rerun = not st.session_state.trigger_rerun  # Force rerun for page transition
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.current_page == "answer_page":
        selected_email = st.session_state.selected_email
        if selected_email:
            st.title(f"Reply to {selected_email['author_name']} &lt;{selected_email['author_email']}&gt;")
            st.write(f"**Subject:** Re: {selected_email['subject']}")
            with st.expander("Show Email Content"):
                components.html(f"<div style='color: white;'>{selected_email['body']}</div>", height=300, scrolling=True)

            st.write("### Compose your reply")
            subject = st.text_input("Your Subject", value=f"Re: {selected_email['subject']}")
            reply_message = st.text_area("Your message", value="Mensagem padrão de resposta para EMAILS")

            if st.button("Send Reply"):
                if reply_message:
                    recipient_email = selected_email['author_email']
                    success = send_reply(st.session_state.user_email, st.session_state.user_password, recipient_email, subject, reply_message)
                    if success:
                        st.success(f"Reply sent to {recipient_email}!")
                        st.session_state.current_page = "email_list"
                        st.session_state.trigger_rerun = not st.session_state.trigger_rerun  # Force rerun back to email list
                    else:
                        st.error("Failed to send reply.")
                else:
                    st.error("Please enter a reply message before sending.")
            if st.button("Return"):
                st.session_state.current_page = "email_list"
                st.session_state.trigger_rerun = not st.session_state.trigger_rerun  # Force rerun back to email list


