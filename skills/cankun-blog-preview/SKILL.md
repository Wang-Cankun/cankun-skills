---
name: cankun-blog-preview
group: internal
summary: >-
  Generates and integrates exactly one Franklin Booth-inspired, white-background
  preview image for a Cankun blog article, then validates its optimized WebP and
  full-resolution link.
description: >-
  Generate and integrate exactly one article preview image for cankun-blog by
  inferring one visual metaphor from a target MDX post, maintaining the Franklin
  Booth-inspired neutral-white series, updating the prompt manifest, creating
  the 2000×800 PNG original, running the repository optimizer for the 1400×560
  WebP, wiring bilingual alt text and the full-resolution link, validating, and
  optionally publishing. Use when the user asks to add, make, generate, refresh,
  replace, or remake a preview, hero, or cover image for one existing or newly
  added cankun-blog article.
---

# Generate one Cankun blog preview

Treat one article slug, including its English and Chinese MDX pair, as the complete transaction. Never turn a single-article request into an archive-wide regeneration.

## Preflight

1. Confirm the workspace is `cankun-blog` and contains:
   - `content/files/`
   - `content/preview-image-prompts.md`
   - `public/images/`
   - `scripts/optimize-previews.ts`
2. Resolve exactly one target slug. If the user did not name it, select it only when exactly one English MDX article lacks preview metadata; otherwise ask which article.
3. Inspect `git status` and preserve unrelated changes.
4. Check whether the target already has a preview PNG or WebP. Overwrite it only when the user explicitly asked to refresh, replace, remake, or restyle it; otherwise report the existing asset and stop.
5. Remember that `bun run previews` scans every `public/images/**/*-preview.png`. Check for unrelated stale sources before running it; stop and report a scope conflict if the command would regenerate another article's WebP.

## Read the sources of truth

Read the target English article fully. Read its Chinese pair when present so the alternative text can be localized accurately.

Read these repository-owned sources rather than copying their contents into this skill:

- `content/preview-image-prompts.md` — current series contract and per-article prompts.
- `public/images/shape-of-not-knowing/known-unknowns-preview.png` — visual style anchor.
- `scripts/optimize-previews.ts` — the only publication resize and WebP compression implementation.

## Define one visual metaphor

Infer the image from the article's argument, not its title alone. Reduce it to one subject, one action or tension, and one spacious setting. Avoid collages and stacks of symbols.

When no metaphor is clearly strongest, present at most three concrete candidates and ask the user to choose before generating.

Add or update only the target article's block in `content/preview-image-prompts.md`. Preserve the existing prompt structure. Require all of the following:

- An original pen-and-ink illustration inspired by Franklin Booth's engraving-like technique.
- Charcoal-black linework and neutral-gray hatching.
- A clean neutral pure-white (`#ffffff`) paper field continuous to every edge.
- An exact 5:2 panoramic composition with essential subjects in the central horizontal band.
- No warm ivory, cream, beige, sepia, yellow cast, aged paper, stain, parchment tint, or colored wash.
- No text, letters, numbers, labels, logos, border, signature, or watermark.

## Generate exactly one image

Use the available image-generation skill and tool.

- Use the 09 PNG as Image 1 and as a style/composition reference only.
- For an explicit remake, use the current target PNG as Image 2 for subject continuity.
- State that the requested result is a new rendering, not a recolor.
- Generate only the target article's preview.
- Inspect the result before installing it.

Save the full-resolution original under the target article's existing naming convention:

```text
public/images/<article-image-directory>/<name>-preview.png
```

The installed PNG must be exactly 2000×800. If the image tool returns a nearby unsupported canvas size, perform one high-quality crop/scale to normalize the PNG. This normalization is only for the full-resolution source; do not create or resize the publication WebP manually.

## Integrate the article

In both MDX language variants when present:

- Set `meta.preview` to the adjacent `.webp` URL.
- Write a concise, literal `meta.previewAlt` in that language.

Do not edit shared article components when they already derive the adjacent PNG link and render the alternative text as the figure description. Change shared code only when the existing contract cannot support the target article.

## Generate the publication asset

Run only the repository entry point:

```bash
bun run previews
```

Do not invoke Sharp, ImageMagick, or another encoder to create the WebP. Verify that the target output is adjacent to the PNG, 1400×560, WebP, and newer than its source. Run `bun run previews` again and require the target to be reported up to date.

## Validate

Verify all of the following before handoff:

- Only the target article's prompt, metadata, PNG, and WebP changed, apart from an explicitly necessary shared fix.
- The PNG is 2000×800 and the WebP is 1400×560.
- The archive loads the target `.webp` without a broken image.
- The image's white field visually merges into the page background.
- The article shows the localized short description and a link to the `.png` original.
- The original link opens a 2000×800 image.
- Social metadata uses the 1400×560 WebP dimensions.

Run the focused tests and production build when those commands exist:

```bash
bun test scripts/optimize-previews.test.ts app/preview-image.test.ts
bun run build
```

Use a clean browser session for the archive and target article. Check console errors and broken images.

## Publish only on request

Do not commit, push, or deploy unless the user explicitly asks to publish. When publishing is requested:

1. Stage only the intended article-preview changes.
2. Commit and push the current branch according to repository convention.
3. Verify the live WebP, article caption, and PNG original rather than assuming deployment succeeded.

Report the target slug, installed paths, dimensions and sizes, optimizer first/second-run result, validation result, and live URL when published.
