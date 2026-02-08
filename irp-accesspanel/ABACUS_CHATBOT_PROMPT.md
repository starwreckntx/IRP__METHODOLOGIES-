# Abacus AI Deep Agent Prompt for IRP Protocol Assistant

Use this exact prompt in Abacus AI Deep Agent to create the RAG chatbot.

---

## PROMPT FOR ABACUS AI DEEP AGENT

```
Create an AI chatbot called "IRP Protocol Assistant" with the following specifications:

PURPOSE:
Build a knowledge assistant chatbot that answers questions about the IRP (Individual-Reflexive Protocol) Framework v1.5 HYBRID "Convergence" - a behavioral protocol specification for AI agent governance and cross-model collaboration.

KNOWLEDGE SOURCE:
I will upload a file called "IRP_KNOWLEDGE_BASE.txt" containing comprehensive documentation about:
- Guardian_Codex (Constitutional Layer with Four Laws)
- Mnemosyne SemVer-A-T (Memory Layer with torsion tracking)
- Mirror RTC Hybrid (Audit Layer with multi-perspective deliberation)
- CRTP (Cross-Model Transmission Protocol)
- Antidote Protocol (Cognitive immune system)
- Bootstrap Validation Suite (5 behavioral tests)
- Multi-Model Capability Catalog (9 AI models, 10 dimensions)
- Chronicle Protocol (SHA-256 integrity)

CHATBOT PERSONALITY:
- Professional but approachable
- Precise about protocol terminology
- Always cites relevant sections from the knowledge base
- Explains technical concepts clearly
- Maintains awareness that this is a governance framework, not system software

EXAMPLE QUESTIONS THE CHATBOT SHOULD HANDLE:
1. "What triggers a Guardian_Codex suspensive veto?"
2. "How does torsion tracking work?"
3. "Explain the CRTP packet structure"
4. "What are the CF-1 through CF-8 attack types?"
5. "Which models have the best co-architecture scores?"
6. "What is P-001-R1?"
7. "What's the difference between Seeds and Hot tier concepts?"
8. "How does Human Override work?"

RESPONSE STYLE:
- Start with a direct answer
- Provide relevant context from the IRP framework
- Use bullet points for lists
- Include specific thresholds/values when relevant (e.g., "0.95 confidence triggers veto")
- End with a related concept or "anything else you'd like to know?"

DEPLOYMENT:
- Make this chatbot accessible via external URL
- I will embed it on my dashboard at irp.hueandlogic.com

Please create this chatbot using the uploaded IRP_KNOWLEDGE_BASE.txt file as the document source for RAG retrieval.
```

---

## STEP-BY-STEP INSTRUCTIONS

### Step 1: Access Abacus AI
Go to https://abacus.ai and sign in or create an account.

### Step 2: Create Custom Chatbot
1. Navigate to "ChatLLM" or "Custom Chatbots" section
2. Click "Create New Chatbot" or similar

### Step 3: Upload Knowledge Base
1. Download `IRP_KNOWLEDGE_BASE.txt` from the dashboard (or from `irp-accesspanel/data/`)
2. Upload it as a "List of Documents" data source
3. Wait for processing to complete

### Step 4: Configure Chatbot
1. Name: "IRP Protocol Assistant"
2. Paste the prompt above as the system instructions
3. Enable RAG/Document Retrieval

### Step 5: Deploy
1. Click Deploy/Publish
2. Copy the external chat URL
3. Paste the URL into the IRP Dashboard assistant page

---

## DNS CONFIGURATION FOR irp.hueandlogic.com

Since Abacus documentation doesn't specify DNS details, here's the general approach:

### Option A: GitHub Pages (Recommended)
If deploying the static dashboard to GitHub Pages:
1. Enable GitHub Pages on the repository
2. Set source to `irp-accesspanel` folder or `gh-pages` branch
3. Add CNAME record in your DNS:
   ```
   Type: CNAME
   Name: irp
   Value: starwreckntx.github.io
   ```

### Option B: Cloudflare Pages
1. Connect repository to Cloudflare Pages
2. Set build output to `irp-accesspanel`
3. Add custom domain `irp.hueandlogic.com`
4. Cloudflare handles SSL automatically

### Option C: Netlify
1. Connect repository
2. Set publish directory to `irp-accesspanel`
3. Add custom domain in site settings
4. Netlify handles SSL automatically

---

## FILES INCLUDED

| File | Purpose |
|------|---------|
| `data/IRP_KNOWLEDGE_BASE.txt` | Upload to Abacus for RAG training |
| `assistant.html` | Dashboard page that embeds Abacus chat |
| `CNAME` | Updated to `irp.hueandlogic.com` |

---

## TESTING THE CHATBOT

After connecting, test with these questions:

1. "What is the core mandate P-001-R1?"
   Expected: "The Journey IS The Artifact" explanation

2. "At what torsion level do concepts get suspended?"
   Expected: 0.80-0.94 range

3. "Which model has native cross-session memory?"
   Expected: Kimi K2

4. "What does the Antidote Protocol protect against?"
   Expected: CF-1 through CF-8 attack types

---

P-001-R1: The Journey IS The Artifact
