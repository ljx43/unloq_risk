# Go Early Risk SQL Skill - Encrypted Viewer

This folder contains a public-safe encrypted viewer for the Go Early Risk SQL skill and dictionaries.

## How It Works

- `index.html` contains encrypted ciphertext only.
- The password is not stored in this repository.
- Decryption happens locally in the browser using Web Crypto.
- After unlocking, the page displays the bundled Markdown/YAML files and lets you copy or download each file.

## Security Notes

- Keep the password outside GitHub.
- Use a strong password.
- Anyone can download the ciphertext from a public repository, so weak passwords can be brute-forced.
- For stronger access control, use a private repository or an external access layer such as Cloudflare Access.
