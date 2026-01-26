# Craft Product Image Generator

This tool generates product photography using DALL-E 3 based on your photography shot list requirements.

## Setup

1. **Create a `.env` file** (never commit this to git):
```
OPENAI_API_KEY=your_api_key_here
```

2. **Install dependencies:**
```bash
pip install openai python-dotenv requests
```

3. **Run the generator:**
```bash
python generate_images.py
```

## Security

- Never commit `.env` files or API keys to git
- The `.gitignore` file excludes `.env` automatically
- Use environment variables in production

## Image Prompts

The generator uses carefully crafted prompts based on the photography shot list to create:
- PTFE cover sheet product photos
- Release paper usage demonstrations
- Diamond painting supply images
- Lifestyle and use-case photography
