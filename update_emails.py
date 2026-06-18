#!/usr/bin/env python3
"""
Update coach folder with correct CoachJVTech email addresses
"""
import os
from pathlib import Path

COACH_DIR = "/home/ubuntu/coach"

# Email mappings - keeping support@ as the main one, but documenting all
CORRECT_EMAILS = {
    'support': 'support@coachjvtech.us',
    'admin': 'admin@coachjvtech.us',
    'billing': 'billing@coachjvtech.us',
}

def update_env_example():
    """Update .env.example with all email addresses"""
    env_file = Path(COACH_DIR) / '.env.example'
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Update Zoho email
        content = content.replace('ZOHO_EMAIL=support@coachjvtech.us', 
                                 f'ZOHO_EMAIL={CORRECT_EMAILS["support"]}')
        
        # Add comments for other emails if not present
        if 'admin@coachjvtech.us' not in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'ZOHO_FROM_NAME' in line:
                    lines.insert(i+1, '')
                    lines.insert(i+2, '# Additional email addresses:')
                    lines.insert(i+3, f'# Admin: {CORRECT_EMAILS["admin"]}')
                    lines.insert(i+4, f'# Billing: {CORRECT_EMAILS["billing"]}')
                    break
            content = '\n'.join(lines)
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print(f"✓ Updated: .env.example")

def update_settings():
    """Update settings.py DEFAULT_FROM_EMAIL"""
    settings_file = Path(COACH_DIR) / 'coach' / 'settings.py'
    
    if settings_file.exists():
        with open(settings_file, 'r') as f:
            content = f.read()
        
        # Update DEFAULT_FROM_EMAIL
        new_email_line = f"DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'CoachJVTech <{CORRECT_EMAILS['support']}>')"
        content = content.replace(
            "DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'Coach CryptoTrade <noreply@coachcrypto.com>')",
            new_email_line
        )
        
        with open(settings_file, 'w') as f:
            f.write(content)
        
        print(f"✓ Updated: coach/settings.py")

def update_documentation():
    """Update documentation files with correct emails"""
    doc_files = [
        'EMAIL_AUTH_SETUP.md',
        'ZOHO_EMAIL_SETUP_GUIDE.md',
        'README.md',
        'QUICK_REFERENCE.txt',
        'PROJECT_SUMMARY.md',
        'IMPLEMENTATION_COMPLETE.txt'
    ]
    
    for doc_file in doc_files:
        file_path = Path(COACH_DIR) / doc_file
        if file_path.exists():
            with open(file_path, 'r') as f:
                content = f.read()
            
            original = content
            
            # Ensure support@ is correct
            if 'support@coachjvtech.us' in content or 'support@' in content:
                # Already updated or generic, make sure it's the right domain
                pass
            
            # Add admin and billing references where appropriate
            if 'support@coachjvtech.us' in content and 'admin@coachjvtech.us' not in content:
                # This is an email config file, add other addresses
                if 'EMAIL' in doc_file.upper() or 'ZOHO' in doc_file.upper():
                    content += f"\n\n## Additional Email Addresses\n"
                    content += f"- Support: {CORRECT_EMAILS['support']}\n"
                    content += f"- Admin: {CORRECT_EMAILS['admin']}\n"
                    content += f"- Billing: {CORRECT_EMAILS['billing']}\n"
            
            if content != original:
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"✓ Updated: {doc_file}")

def create_email_reference():
    """Create a reference file with all email addresses"""
    email_ref = Path(COACH_DIR) / 'COACHJVTECH_EMAILS.md'
    
    content = f"""# CoachJVTech Email Addresses

## Official Email Addresses

All email addresses use the domain: **coachjvtech.us**

### Primary Contact Emails

1. **Support Email**
   - Address: {CORRECT_EMAILS['support']}
   - Purpose: Customer support, general inquiries, help requests
   - Usage: Contact forms, support tickets, help documentation

2. **Admin Email**
   - Address: {CORRECT_EMAILS['admin']}
   - Purpose: Administrative communications, account management
   - Usage: User registration confirmations, account updates, admin notifications

3. **Billing Email**
   - Address: {CORRECT_EMAILS['billing']}
   - Purpose: Payment inquiries, subscription management, invoices
   - Usage: Payment confirmations, billing issues, subscription notifications

## Configuration

### Django Settings
```python
DEFAULT_FROM_EMAIL = 'CoachJVTech <{CORRECT_EMAILS['support']}>'
SERVER_EMAIL = '{CORRECT_EMAILS['admin']}'
```

### Email Service Configuration

#### Zoho Mail Setup
- Primary account: {CORRECT_EMAILS['support']}
- Configure SMTP for sending emails
- Set up forwarding/aliases for admin@ and billing@

#### Email Templates
All email templates should use:
- From: CoachJVTech <{CORRECT_EMAILS['support']}>
- Reply-To: {CORRECT_EMAILS['support']}>

## Usage in Templates

### Support Links
```html
<a href="mailto:{CORRECT_EMAILS['support']}">Contact Support</a>
```

### Admin Links
```html
<a href="mailto:{CORRECT_EMAILS['admin']}">Contact Admin</a>
```

### Billing Links
```html
<a href="mailto:{CORRECT_EMAILS['billing']}">Billing Inquiries</a>
```

---
**Domain:** coachjvtech.us  
**Branding:** CoachJVTech  
**Updated:** June 5, 2026
"""
    
    with open(email_ref, 'w') as f:
        f.write(content)
    
    print(f"✓ Created: COACHJVTECH_EMAILS.md")

def main():
    print("📧 UPDATING COACHJVTECH EMAIL ADDRESSES")
    print("=" * 70)
    print(f"Support: {CORRECT_EMAILS['support']}")
    print(f"Admin:   {CORRECT_EMAILS['admin']}")
    print(f"Billing: {CORRECT_EMAILS['billing']}")
    print("=" * 70)
    print()
    
    update_env_example()
    update_settings()
    update_documentation()
    create_email_reference()
    
    print("\n" + "=" * 70)
    print("✅ EMAIL ADDRESSES UPDATED!")
    print("=" * 70)

if __name__ == "__main__":
    main()
