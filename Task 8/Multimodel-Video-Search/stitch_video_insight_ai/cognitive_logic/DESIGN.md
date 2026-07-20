---
name: Cognitive Logic
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#434655'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#712ae2'
  on-secondary: '#ffffff'
  secondary-container: '#8a4cfc'
  on-secondary-container: '#fffbff'
  tertiary: '#943700'
  on-tertiary: '#ffffff'
  tertiary-container: '#bc4800'
  on-tertiary-container: '#ffede6'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#eaddff'
  secondary-fixed-dim: '#d2bbff'
  on-secondary-fixed: '#25005a'
  on-secondary-fixed-variant: '#5a00c6'
  tertiary-fixed: '#ffdbcd'
  tertiary-fixed-dim: '#ffb596'
  on-tertiary-fixed: '#360f00'
  on-tertiary-fixed-variant: '#7d2d00'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  body-base:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: '0'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: '0'
  label-upper:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-code:
    fontFamily: jetbrainsMono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  gutter: 24px
  container-max: 1280px
---

## Brand & Style

This design system is built for the next generation of artificial intelligence interfaces. The brand personality is **clinical, intelligent, and unobtrusive**, prioritizing clarity of thought and ease of interaction. By adopting a "Content-First" philosophy, the UI recedes into the background, allowing the generative output and user data to take center stage.

The design style is **Modern Minimalism with Soft Elevation**. It draws inspiration from the precision of developer tools and the approachability of premium consumer SaaS. The emotional response should be one of "effortless power"—providing the user with high-functioning tools that feel light and manageable rather than dense or overwhelming. Use ample whitespace (negative space) to separate distinct cognitive tasks.

## Colors

The palette is anchored in a high-clarity "Paper White" environment. 

- **Primary (AI Blue):** Used for primary actions, active states, and focus indicators. It represents reliability and logical processing.
- **Secondary (Intelligence Purple):** Reserved for "AI-augmented" features, sparkle effects, or generative states. It signals the presence of machine intelligence.
- **Neutrals (Slate Grays):** We utilize a Slate scale for typography and borders. #0f172a (Slate 950) is used for headings to ensure maximum contrast and legibility, while #64748b (Slate 500) handles secondary metadata.
- **Accents:** Use subtle 5% - 10% opacity tints of the primary and secondary colors for background washes on cards or active menu items.

## Typography

This design system utilizes **Inter** for all UI elements to maintain a systematic, utilitarian aesthetic. 

- **Tight Tracking:** Headlines should use a slight negative letter spacing (-0.01em to -0.02em) to appear more cohesive and professional.
- **Hierarchy:** Use font weight rather than size to distinguish hierarchy where possible. Bold (700) for headers, Medium (500) for buttons, and Regular (400) for long-form body text.
- **Code Blocks:** For AI prompts or technical output, switch to **JetBrains Mono** to provide a clear visual distinction from the conversational UI.
- **Readability:** Ensure line heights for body text are never below 1.5x the font size to maintain the "airy" feel of the design narrative.

## Layout & Spacing

The layout philosophy is a **Structured Fluid Grid**. We use an 8px base unit to drive all spatial decisions.

- **Desktop:** 12-column grid with 24px gutters and 48px side margins. 
- **Tablet:** 8-column grid with 24px gutters and 24px side margins.
- **Mobile:** 4-column grid with 16px gutters and 16px side margins.

Maintain consistent vertical rhythm by using `lg` (24px) spacing between major sections and `md` (16px) for internal component padding. Use `3xl` (64px) or more for top/bottom section padding to reinforce the "minimalist/airy" brand pillar.

## Elevation & Depth

We avoid heavy drop shadows in favor of **Tonal Layering** and **Ambient Depth**. 

1. **Surface Level (Level 0):** Pure White (#FFFFFF).
2. **Container Level (Level 1):** Slate 50 (#F8FAFC) or a 1px border of Slate 200 (#E2E8F0).
3. **Soft Elevation (Level 2):** Used for cards and modals. A very diffused shadow: `0px 4px 12px rgba(15, 23, 42, 0.03), 0px 1px 2px rgba(15, 23, 42, 0.06)`.

The goal is for elements to feel like they are resting lightly on the page, rather than floating far above it. Use subtle backdrop blurs (8px to 12px) for sticky headers and navigation overlays to maintain context of the content underneath.

## Shapes

The design system uses a **Large-Radius Geometry** to soften the technical nature of the AI product. 

- **Standard Elements:** Buttons, input fields, and small widgets use `rounded-lg` (0.5rem / 8px).
- **Primary Containers:** Cards, modals, and main content areas use `rounded-2xl` (1rem / 16px).
- **Speciality Components:** AI chat bubbles and featured marketing cards may use `rounded-3xl` (1.5rem / 24px) to emphasize the friendly, modern aesthetic.

Icons should always use a rounded cap and join (round/round) to match the curvature of the UI components.

## Components

### Buttons
- **Primary:** Solid AI Blue (#2563eb) with White text. High-contrast, 8px border radius.
- **Secondary:** Slate 100 background with Slate 900 text. Becomes Slate 200 on hover.
- **AI Action:** Gradient border or subtle Intelligence Purple (#7c3aed) glow to indicate generative capabilities.

### Input Fields
- **Default:** White background, 1px Slate 200 border. 
- **Focus:** Border changes to AI Blue with a 3px soft outer halo of the same color at 10% opacity.
- **Prompt Bars:** Larger 16px padding with 24px border radius (capsule style) to denote the main AI interaction point.

### Cards
- White background, 1px Slate 100 border, and the "Level 2" soft shadow. 
- Internal padding should be a minimum of 24px (`lg`) to keep content legible.

### Chips & Badges
- Small, uppercase labels with 12px font size.
- Use low-saturation background tints (e.g., Blue 50 background for Blue 700 text).

### Icons
- Use **Lucide** icons with a 2px stroke width. 
- Icons should be sized to 20px within a 24px bounding box for optimal alignment with Inter 16px text.