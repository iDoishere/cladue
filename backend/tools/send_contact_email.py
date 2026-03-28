import json
import os
import re

# Rate limiting — max 1 email per session
_sent_sessions: set = set()


def _sanitize(text: str) -> str:
    """Strip HTML tags to prevent injection."""
    return re.sub(r'<[^>]+>', '', text).strip()


def send_contact_email(
    sender_name: str,
    sender_email: str,
    sender_company: str,
    message: str,
    session_id: str = "unknown"
) -> str:
    """
    Send a contact email to Ido Cohen from a recruiter or visitor.
    Use this tool ONLY after collecting all required information from the user:
    - sender_name: their full name
    - sender_email: their email address (so Ido can reply)
    - sender_company: their company name
    - message: their message to Ido
    - session_id: the current session ID (pass this automatically)

    Returns JSON with success status.
    """
    # Rate limit — one email per session
    if session_id in _sent_sessions:
        return json.dumps({
            "success": False,
            "error": "already_sent",
            "message": "An email was already sent in this session."
        })

    # Validate email format
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', sender_email):
        return json.dumps({
            "success": False,
            "error": "invalid_email",
            "message": "The email address provided doesn't look valid."
        })

    # Sanitize inputs
    name    = _sanitize(sender_name)
    email   = _sanitize(sender_email)
    company = _sanitize(sender_company)
    body    = _sanitize(message)

    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        return json.dumps({
            "success": False,
            "error": "not_configured",
            "message": "Email service is not configured."
        })

    try:
        import resend
        resend.api_key = api_key

        html_body = f"""
        <div style="font-family: -apple-system, sans-serif; max-width: 560px; margin: 0 auto; padding: 32px; background: #0f0f0f; color: #f0f0f0; border-radius: 12px;">
          <div style="margin-bottom: 24px;">
            <span style="background: #7c3aed; color: white; font-size: 12px; padding: 4px 10px; border-radius: 20px; letter-spacing: 1px;">PORTFOLIO CONTACT</span>
          </div>
          <h2 style="margin: 0 0 24px; font-size: 22px; color: #fff;">New message from your portfolio</h2>
          <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px;">
            <tr>
              <td style="padding: 10px 0; color: #888; font-size: 13px; width: 90px;">Name</td>
              <td style="padding: 10px 0; color: #fff; font-size: 14px;">{name}</td>
            </tr>
            <tr>
              <td style="padding: 10px 0; color: #888; font-size: 13px;">Company</td>
              <td style="padding: 10px 0; color: #fff; font-size: 14px;">{company}</td>
            </tr>
            <tr>
              <td style="padding: 10px 0; color: #888; font-size: 13px;">Email</td>
              <td style="padding: 10px 0; font-size: 14px;"><a href="mailto:{email}" style="color: #a78bfa;">{email}</a></td>
            </tr>
          </table>
          <div style="background: #1a1a1a; border-left: 3px solid #7c3aed; padding: 16px 20px; border-radius: 0 8px 8px 0;">
            <p style="margin: 0; color: #ccc; font-size: 14px; line-height: 1.7;">{body}</p>
          </div>
          <p style="margin-top: 24px; color: #555; font-size: 12px;">Sent via AI Portfolio · Just hit reply to respond</p>
        </div>
        """

        resend.Emails.send({
            "from":     "Portfolio <onboarding@resend.dev>",
            "to":       ["idoishere2@gmail.com"],
            "reply_to": email,
            "subject":  f"Portfolio Contact: {name} from {company}",
            "html":     html_body,
        })

        _sent_sessions.add(session_id)

        return json.dumps({
            "success": True,
            "message": f"Email sent successfully to Ido from {name} ({company})."
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "message": "Failed to send email. Please try again."
        })
