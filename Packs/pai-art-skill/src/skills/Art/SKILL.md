---
name: Art
description: Complete visual content system. USE WHEN user wants to create visual content, illustrations, diagrams, OR mentions art, header images, visualizations, mermaid, flowchart, technical diagram, infographic, PAI icon, pack icon, or PAI pack icon.
---

# Art Skill

Complete visual content system for creating illustrations, diagrams, and visual content.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/CORE/USER/SKILLCUSTOMIZATIONS/Art/`

If this directory exists, load and apply:
- `PREFERENCES.md` - Aesthetic preferences, default model, output location
- `CharacterSpecs.md` - Character design specifications
- `SceneConstruction.md` - Scene composition guidelines

These override default behavior. If the directory does not exist, proceed with skill defaults.

## MANDATORY: Output to Downloads First

```
ALL GENERATED IMAGES GO TO ~/Downloads/ FIRST
NEVER output directly to project directories
User MUST preview in Finder/Preview before use
```

**This applies to ALL workflows in this skill.**

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow from the Art skill"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow from the **Art** skill...
   ```

---

## Workflow Routing

Route to the appropriate workflow based on the request.

  - Blog header or editorial illustration -> `Workflows/Essay.md`
  - Visualization or chart -> `Workflows/Visualize.md`
  - Mermaid flowchart or sequence diagram -> `Workflows/Mermaid.md`
  - Technical or architecture diagram -> `Workflows/TechnicalDiagrams.md`
  - Framework or 2x2 matrix -> `Workflows/Frameworks.md`
  - Stat card or big number visual -> `Workflows/Stats.md`
  - PAI pack icon -> `Workflows/CreatePAIPackIcon.md`

---

## Core Aesthetic

**Default:** Production-quality concept art style appropriate for editorial and technical content.

**UL Editorial Color Palette:**
```
Background: Light Cream #F5E6D3 or White #FFFFFF
Primary Accent: Deep Purple #4A148C (strategic, 10-20%)
Secondary Accent: Deep Teal #00796B (5-10%)
Structure: Black #000000
Text: Charcoal #2D2D2D
```

**Typography System (3-Tier):**
- Tier 1 (Headers): Valkyrie-style elegant wedge-serif italic
- Tier 2 (Labels): Concourse-style geometric sans-serif
- Tier 3 (Insights): Advocate-style condensed italic for callouts

**Load customizations from:** `~/.claude/skills/CORE/USER/SKILLCUSTOMIZATIONS/Art/PREFERENCES.md`

---

## Image Generation

**Default model:** Check user customization at `SKILLCUSTOMIZATIONS/Art/PREFERENCES.md`
**Fallback:** nano-banana-pro (best text rendering)

### Available Models

| Model | Provider | Best For | Features |
|-------|----------|----------|----------|
| **modelscope** | ModelScope (Tongyi MAI) | Chinese prompts, culturally accurate content | Excellent Chinese language understanding, async API |
| **nano-banana-pro** | Google Gemini | High-quality text rendering, reference images | Up to 14 reference images, 1K-4K resolution |
| **flux** | Replicate | General purpose, fast generation | Multiple aspect ratios, reliable |
| **nano-banana** | Replicate | Fast generation, good quality | Quick iterations, standard quality |
| **gpt-image-1** | OpenAI | Portrait orientation, DALL-E 3 | 1024x1024, 1536x1024, 1024x1536 sizes |

### CRITICAL: Always Output to Downloads First

**ALL generated images MUST go to `~/Downloads/` first for preview and selection.**

Never output directly to a project's `public/images/` directory. User needs to review images in Preview before they're used.

**Workflow:**
1. Generate to `~/Downloads/[descriptive-name].png`
2. User reviews in Preview
3. If approved, THEN copy to final destination
4. Create WebP and thumbnail versions at final destination

```bash
# CORRECT - Output to Downloads for preview
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "[PROMPT]" \
  --size 2K \
  --aspect-ratio 1:1 \
  --thumbnail \
  --output ~/Downloads/blog-header-concept.png

# After approval, copy to final location
cp ~/Downloads/blog-header-concept.png ~/Projects/Website/cms/public/images/
```

### Multiple Reference Images (Character/Style Consistency)

For improved character or style consistency, use multiple `--reference-image` flags:

```bash
# Multiple reference images for better likeness
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model nano-banana-pro \
  --prompt "Person from references at a party..." \
  --reference-image face1.jpg \
  --reference-image face2.jpg \
  --reference-image face3.jpg \
  --size 2K \
  --aspect-ratio 16:9 \
  --output ~/Downloads/character-scene.png
```

**API keys in:** `${PAI_DIR}/.env`

### ModelScope Integration

ModelScope (Tongyi MAI Z-Image Turbo) is now integrated as a first-class model option:

```bash
# Generate with ModelScope (best for Chinese prompts)
bun run ~/.claude/skills/Art/Tools/Generate.ts \
  --model modelscope \
  --prompt "一只可爱的金色小猫，坐在柔软的垫子上" \
  --size 16:9 \
  --output ~/Downloads/chinese-cat.png
```

**Environment variables required:**
- `MODELSCOPE_API_KEY` - Get from https://api-inference.modelscope.cn/
- `REPLICATE_API_TOKEN` - For flux, nano-banana models
- `GOOGLE_API_KEY` - For nano-banana-pro model
- `OPENAI_API_KEY` - For gpt-image-1 model
- `REMOVEBG_API_KEY` - For --remove-bg flag

**ModelScope features:**
- Excellent Chinese language understanding
- Async task API (polls for completion)
- Culturally accurate content generation
- Standard aspect ratios (1:1, 16:9, 3:2, etc.)

## Examples

**Example 1: Blog header image**
```
User: "create a header for my AI agents post"
-> Invokes ESSAY workflow
-> Generates editorial illustration prompt
-> Creates image with consistent aesthetic
-> Saves to ~/Downloads/ for preview
-> After approval, copies to public/images/
```

**Example 2: Technical architecture diagram**
```
User: "make a diagram showing the SPQA pattern"
-> Invokes TECHNICALDIAGRAMS workflow
-> Creates structured architecture visual
-> Outputs PNG with consistent styling
```

**Example 3: Framework visualization**
```
User: "create a 2x2 matrix for security vs convenience"
-> Invokes FRAMEWORKS workflow
-> Creates hand-drawn framework visual
-> Purple highlights optimal quadrant
```

**Example 4: PAI pack icon**
```
User: "create icon for the skill system pack"
-> Invokes CREATEPAIPACKICON workflow
-> Generates 1K image with --remove-bg for transparency
-> Resizes to 256x256 RGBA PNG
-> Outputs to ~/Downloads/ for preview
```
