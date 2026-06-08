---
name: figma-theme-factory
description: Toolkit for styling Figma designs with a theme. Apply a cohesive color palette and font pairing to any Figma file, frame, or component set — landing pages, app screens, design systems, dashboards, decks. There are 100 pre-set themes, each with a curated palette and header/body font pairing, or generate a new theme on-the-fly when none fit.
---


# Figma Theme Factory Skill

This skill provides a curated collection of 100 professional themes, each with a carefully selected color palette and font pairing. Once a theme is chosen, it can be applied to any Figma design as variables, text styles, and layer bindings.

## Purpose

To apply consistent, professional styling to a Figma file — landing pages, app screens, dashboards, design-system foundations, or slide layouts — use this skill. Each theme includes:
- A cohesive four-color palette with hex codes
- A defined role for each color (background, body text, primary accent, secondary accent)
- A complementary header/body font pairing
- A distinct visual identity suited to a specific context and audience

## Usage Instructions

To apply a theme to a Figma design:

1. **Show the theme showcase**: Display the `theme_showcase.pdf` file so the user can browse all 100 themes visually. Do not modify it; simply show the file for viewing.
2. **Ask for their choice**: Ask which theme to apply, and to which file/frame/page.
3. **Wait for selection**: Get explicit confirmation of the chosen theme before applying anything.
4. **Apply the theme**: Read the corresponding theme file from the `themes/` directory and apply its colors and fonts to the target design (see Application Process below).

## How Themes Map to Figma

Every theme defines four roles. Translate them to Figma primitives so the styling is reusable and swappable:

| Theme role | Figma primitive | Where it goes |
| --- | --- | --- |
| Background | `color/background` variable | Page/frame fills, section and card backgrounds |
| Body Text | `color/text` variable | Paragraphs, labels, captions, default text fills |
| Primary Accent | `color/accent-primary` variable | Buttons, links, primary CTAs, key emphasis |
| Secondary Accent | `color/accent-secondary` variable | Badges, chart series, dividers, supporting details |
| Header font | `text/heading` text style | Titles and section headers |
| Body font | `text/body` text style | Body copy, captions, UI labels |

Bundle the four color variables in one variable collection named `Theme` so the whole design can be re-themed by swapping values in a single place.

## Themes Available

All 100 themes are showcased in `theme_showcase.pdf` and specified individually in the `themes/` directory. They are grouped into seven families by mood and intended use:

### Professional — polished, reliable, business-ready

- **Stormy Morning** (`stormy-morning.md`) — #6A89A7 #BDDDFC #88BDF2 #384959
- **Chili Spice** (`chili-spice.md`) — #CD1C18 #FFA896 #9B1313 #38000A
- **Chocolate Truffle** (`chocolate-truffle.md`) — #713600 #C05800 #FDFBD4 #38240D
- **Ink Wash** (`ink-wash.md`) — #4A4A4A #CBCBCB #FFFFE3 #6D8196
- **Golden Taupe** (`golden-taupe.md`) — #D4AF37 #BDB76B #FDFBD4 #CE8946
- **Burnt Sienna** (`burnt-sienna.md`) — #E35336 #F5F5DC #F4A460 #A0522D

### Neutral — balanced, refined, quietly sophisticated

- **Salt and Pepper** (`salt-and-pepper.md`) — #FFFFFF #D4D4D4 #B3B3B3 #2B2B2B
- **Quite Clear** (`quite-clear.md`) — #CBCBCB #F2F2F2 #174D38 #4D1717
- **Yacht Club** (`yacht-club.md`) — #F2F0EF #BBBDBC #245F73 #733E24
- **Quiet Luxury** (`quiet-luxury.md`) — #F7E6CA #E8D59E #D9BBB0 #AD9C8E
- **Night Sands** (`night-sands.md`) — #CBBD93 #FAE8B4 #80775C #574A24
- **Harbor Haze** (`harbor-haze.md`) — #909EAE #5C8DC5 #AD9E90 #736F60
- **Old Photograph** (`old-photograph.md`) — #FDFBD4 #D9D7B6 #878672 #545333
- **Cappuccino** (`cappuccino.md`) — #D6B588 #C6C0B9 #705E46 #422701
- **Breakfast Tea** (`breakfast-tea.md`) — #FFD3AC #CCBEB1 #664036 #331008
- **Cozy Campfire** (`cozy-campfire.md`) — #895129 #AD7A32 #8A6E29 #660F09
- **Stone Path** (`stone-path.md`) — #A49A87 #A5A58D #968F83 #E8E5DF
- **Desert Mirage** (`desert-mirage.md`) — #C2B280 #E35336 #98A869 #272757
- **Honeycomb** (`honeycomb.md`) — #FFC107 #F9E076 #FFFDD0 #895129
- **Urban Loft** (`urban-loft.md`) — #0C0A1A #A35E47 #000000 #464646
- **Spiced Mocha** (`spiced-mocha.md`) — #6F4E37 #D47E30 #F5F5DC #6D3B07
- **Siltstone** (`siltstone.md`) — #CBBD93 #FFF5B8 #FFB16E #CCA25A

### Calm — airy, tranquil, focused

- **Blue Eclipse** (`blue-eclipse.md`) — #272757 #8686AC #505081 #0F0E47
- **Charming Seaside** (`charming-seaside.md`) — #B3EBF2 #85D1DB #B6F2D1 #C0FDF2
- **Calm Blue** (`calm-blue.md`) — #90D5FF #57B0FF #77B1D4 #517891
- **Beachfront Views** (`beachfront-views.md`) — #EDE8D0 #6E632E #DBD1ED #ABBEED
- **Under the Moonlight** (`under-the-moonlight.md`) — #CCCCFF #A3A3CC #5C5C99 #292966
- **Minty Fresh** (`minty-fresh.md`) — #98FBCB #BFFFED #7FCFA8 #558B71
- **Retro Calm** (`retro-calm.md`) — #81D8D0 #D99E82 #D7D982 #AE82D9
- **Emerald Odyssey** (`emerald-odyssey.md`) — #00674F #73E6CB #3EBB9E #0A3C30
- **Ocean Tide** (`ocean-tide.md`) — #00D1D1 #4052D6 #00ADAD #005C5C
- **Mountain Mist** (`mountain-mist.md`) — #6D8196 #B0C4DE #01796F #5A5A5A
- **Morning Dew** (`morning-dew.md`) — #AFEEEE #ADEBB3 #C4C4C4 #D3D3D3
- **Frozen Lake** (`frozen-lake.md`) — #6D8196 #ADD8E6 #FFFAFA #000080
- **Coastal Morning** (`coastal-morning.md`) — #93C572 #89CFF0 #F5F5DC #82C8E5

### Nature — organic, restorative, grounded

- **Mossy Hollow** (`mossy-hollow.md`) — #636B2F #BAC095 #D4DE95 #3D4127
- **Lush Forest** (`lush-forest.md`) — #2E6F40 #CFFFDC #68BA7F #253D2C
- **Green Juice** (`green-juice.md`) — #4CBB17 #48872B #39542C #293325
- **Olive Grove** (`olive-grove.md`) — #808000 #228B22 #636B2F #F2F0EF
- **Eucalyptus Grove** (`eucalyptus-grove.md`) — #B2AC88 #898989 #F2F0EF #4B6E48
- **Soft Spring** (`soft-spring.md`) — #6395EE #90B8D6 #88CFA8 #85DECB
- **Autumn Leaves** (`autumn-leaves.md`) — #FFB343 #DB9A39 #B37E2E #614419
- **Winter Chill** (`winter-chill.md`) — #B8E3E9 #93B1B5 #4F7C82 #0B2E33
- **Spring Energy** (`spring-energy.md`) — #89F336 #FFFC30 #4FE0CB #00BF33
- **Pumpkin Spice Season** (`pumpkin-spice-season.md`) — #BE5103 #8C4C1F #544823 #332216
- **Island Oasis** (`island-oasis.md`) — #CCFF00 #FFF37E #9DE05A #FFAE25
- **Autumn Orchard** (`autumn-orchard.md`) — #BEA58E #DAA520 #2E6F40 #660033
- **Tropical Rainforest** (`tropical-rainforest.md`) — #50C878 #7E8C54 #4F7942 #71AA34
- **Wildflower Meadow** (`wildflower-meadow.md`) — #FBF9E7 #FDB813 #82C8E5 #7CFC00
- **Harvest Moon** (`harvest-moon.md`) — #800020 #FFCE1B #A52A2A #BE5103
- **Winter Berry** (`winter-berry.md`) — #8E0A1E #2E6F40 #ADD8E6 #FFFFFF
- **Summer Breeze** (`summer-breeze.md`) — #FFEB3B #F88379 #82C8E5 #E6D8C4

### Romantic — soft, expressive, inviting

- **Wisteria Bloom** (`wisteria-bloom.md`) — #D3D3FF #9400D3 #D8BFD8 #ED80E9
- **Blooming Romance** (`blooming-romance.md`) — #660033 #E673AC #469110 #00520A
- **Desert Dusk** (`desert-dusk.md`) — #A2574F #E68057 #BF7587 #993A8B
- **Lavender Fields** (`lavender-fields.md`) — #FDFBD4 #BDB96A #C1BFFF #CF6DFC
- **Hydrangea** (`hydrangea.md`) — #FF8DA1 #FFC2BA #FF9CE9 #AD56C4
- **Cactus Flower** (`cactus-flower.md`) — #E491A6 #845763 #92E4BA #90C67F
- **Wildflowers** (`wildflowers.md`) — #A8DCAB #519755 #DBAAA7 #BE91BE
- **Country Garden** (`country-garden.md`) — #FFFFE3 #DBD4FF #808034 #723480
- **Lotus Garden** (`lotus-garden.md`) — #ADEBB3 #FF857A #EBAEE6 #6B403C
- **Iris Garden** (`iris-garden.md`) — #A47DAB #692475 #82AB7D #6A6B4E
- **Fresh Peach** (`fresh-peach.md`) — #FFD3AC #FFB5AB #E39A7B #DBB06B
- **Golden Hour** (`golden-hour.md`) — #FFBF00 #CFB53B #E0B0FF #ECE9C8
- **Spiced Chai** (`spiced-chai.md`) — #FDFBD4 #D47E30 #8D5A2B #825E34
- **Cherry Blossom** (`cherry-blossom.md`) — #F2C7C7 #FFFFFF #D5F3D8 #FFB7C5
- **Evening Rose** (`evening-rose.md`) — #DCA1A1 #996666 #8E4585 #4A4A4A
- **Pastel Garden** (`pastel-garden.md`) — #C75F71 #F0B8B8 #A2AE9D #54463A
- **Tuscan Sunset** (`tuscan-sunset.md`) — #E35336 #FFD3AC #9988A1 #8A2B0E
- **Cotton Candy Skies** (`cotton-candy-skies.md`) — #B298E7 #B8E3E9 #F5B8D5 #F9BEDD
- **Lavender Lullaby** (`lavender-lullaby.md`) — #B5C7EB #9EF0FF #A4A5F5 #8E70CF
- **Peach Skyline** (`peach-skyline.md`) — #FFDBBB #BADDFF #BAFFF5 #496580

### Playful — bright, energetic, approachable

- **Zesty Lemon** (`zesty-lemon.md`) — #FFFF66 #FFE566 #D6D58B #B3B347
- **California Beaches** (`california-beaches.md`) — #FFC067 #66F4FF #66C4FF #7D99AA
- **Freshly Squeezed** (`freshly-squeezed.md`) — #FFBF00 #F2CF7E #FFE642 #FF7900
- **Pistachio Dream** (`pistachio-dream.md`) — #80EF80 #E3F0A3 #BADBA2 #42D674
- **Mango Popsicle** (`mango-popsicle.md`) — #F2B949 #EDD377 #F2E829 #F27430
- **Guava** (`guava.md`) — #FF8559 #FFB578 #E65447 #CF5376
- **Glowing Horizon** (`glowing-horizon.md`) — #FFB343 #42EAFF #4272FF #FF7E42
- **Sunny Day** (`sunny-day.md`) — #FFBF00 #807040 #007EFF #2400FF
- **Retro Sunset** (`retro-sunset.md`) — #BE5103 #FFCE1B #069494 #B7410E
- **Bubblegum Pop** (`bubblegum-pop.md`) — #FF69B4 #069494 #FFFFFF #00F0FF
- **Watermelon Splash** (`watermelon-splash.md`) — #FC6C85 #89F336 #4A4A4A #ADEBB3

### Vibrant — bold, high-impact, attention-grabbing

- **Electric Kiwi** (`electric-kiwi.md`) — #CCFF00 #FFFF00 #DFFF00 #000000
- **Alchemical Reaction** (`alchemical-reaction.md`) — #9D00FF #DE811D #6BFF00 #5B8040
- **Electropop** (`electropop.md`) — #CCFF00 #FF6B00 #F900FF #5200FF
- **Cool Revival** (`cool-revival.md`) — #00FFFF #00AEFF #00DE94 #00FF52
- **Neon Jungle** (`neon-jungle.md`) — #89F336 #38A711 #F23598 #A835F2
- **Sharp Edge** (`sharp-edge.md`) — #898989 #D9D9D9 #FF4D4D #4DFFBC
- **Electric Fusion** (`electric-fusion.md`) — #00F0FF #00FF81 #FFA900 #FF6800
- **Fireworks** (`fireworks.md`) — #ED2100 #E88A38 #960016 #BF00AC
- **Space Berries** (`space-berries.md`) — #FD3DB5 #FFB8DC #FB6A2C #8C1946
- **Pop Art** (`pop-art.md`) — #00F0FF #FF46A2 #FFFF00 #EE4B2B
- **Urban Graffiti** (`urban-graffiti.md`) — #FF2400 #2CFF05 #00F0FF #5A5A5A
- **Neon Noir** (`neon-noir.md`) — #000000 #2CFF05 #BF00FF #2D2D2D
- **Tropical Punch** (`tropical-punch.md`) — #FF8243 #FFC0CB #FCE883 #069494
- **Cobalt Sky** (`cobalt-sky.md`) — #0047AB #000080 #82C8E5 #6D8196
- **Technicolor Dream** (`technicolor-dream.md`) — #FF00FF #00FFFF #CCFF00 #191970
- **Jewel Box** (`jewel-box.md`) — #50C878 #0F52BA #9966CC #CFB53B
- **Gothic Noir** (`gothic-noir.md`) — #000000 #D1D0D0 #988686 #5C4E4E

## Theme Details

Each theme file in `themes/` contains the complete specification:
- The four-color palette with hex codes and per-color roles
- The full theme-role table (background, body text, primary accent, secondary accent) with usage notes
- The header/body font pairing
- A ready-to-use Figma mapping (variable names and text styles)
- A "Best Used For" note describing ideal contexts

## Application Process

After a theme is selected:

1. **Read the theme file** — open the matching `themes/<slug>.md` for exact hex codes, fonts, and role mapping.
2. **Create the variable collection** — add a `Theme` collection with `color/background`, `color/text`, `color/accent-primary`, and `color/accent-secondary` set to the theme's values.
3. **Create text styles** — define `text/heading` (header font) and `text/body` (body font); load the fonts first if they are not already available in the file.
4. **Bind the layers** — set frame/section fills to `color/background`, text fills to `color/text`, primary interactive and emphasis elements to `color/accent-primary`, and supporting elements to `color/accent-secondary`; apply the two text styles to headings and body copy respectively.
5. **Check contrast and readability** — confirm body text reads clearly on the background and that accent colors remain legible where used on text or icons; nudge usage (e.g., reserve a low-contrast accent for fills rather than text) rather than altering the theme's defined colors.
6. **Keep the identity consistent** — apply the same variables and styles across every frame, page, and component so the theme reads as one system.

## Create Your Own Theme

If none of the 100 themes fit, generate a custom theme in the same shape as the presets:

1. Pick a four-color palette and assign the four roles (background, body text, primary accent, secondary accent), ensuring body text has strong contrast against the background.
2. Choose a header font and a body font that pair well and match the intended mood.
3. Give the theme a descriptive name reflecting its color/mood (e.g., the way "Stormy Morning" or "Neon Noir" describe theirs).
4. Write the description and a "Best Used For" note, and present the full spec for the user to review and verify.
5. Once approved, apply it using the same Application Process above.
