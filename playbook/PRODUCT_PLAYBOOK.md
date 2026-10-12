# Product playbook: how a new product gets into the store

*Written as standing instructions for the AI agent (Claude Code) that runs the weekly product run. The "Limits"
section is the guardrail: the agent never spends money, creates accounts or handles passwords/payment details.*

Run weekly: add 1-2 strong products (0 is fine if nothing passes), then polish the whole store. A product that
doesn't clearly pass every check is skipped, not forced.
Each run is logged (date, products added, products skipped and why, polish notes).

## 1. Find candidates
- Cat products only, for indoor cats. Fill gaps first: categories with few items, things that pair with best sellers.
- Source: AliExpress via DSers. Supplier must **ship from the United States** to New York.
- Skip anything already in the store, in DSers' Import List, or in pricing.json `removed` / dropped.
- Never: cat food, treats, supplements, medicine, flea/tick products, anything with health or vet claims,
  branded/trademarked or look-alike items (Disney, Hello Kitty, brand logos), live plants, sharp/unsafe toys, cheap
  electronics without a clear safety rating.

## 2. Quality checks (all must pass)
- Rating 4.6+ with a meaningful number of reviews (50+); recent reviews with buyer photos that match the listing.
- Delivery to NY within ~10 days; real, clean supplier photos (no other shop's logo/watermark, no Chinese-text-only images).
- Not a "Max. 1 per shopper" listing if another good supplier exists.
- The product looks like something a careful pet store would sell (no flimsy junk, no reviews about smell/breaking).

## 3. Profit check (must pass; if it fails, find a different product)
- Cost = DSers price for the exact variant + shipping to NY (use the DSers number, not AliExpress "new shopper" deals).
- Fees = 2.9% of price + $0.30 (Shopify Payments).
- Price on our store: end in .99, at or below what similar items sell for on Amazon (check Amazon; if Amazon is much
  cheaper, nobody buys from us: skip it).
- Profit = price - cost - fees. Needs **profit >= $10 AND >= 30% of price**. Shipping rule: orders under $35 pay $5.95,
  so cheap items still work, but very cheap items rarely reach $10 profit; skip them rather than overprice.
- Record cost, price, profit, Amazon comparison and the AliExpress link in pricing.json (`products`, cost_source
  "DSers <date>, mapped variant, US") and PRODUCTS.md.

## 4. Add to Shopify (via DSers push, then clean up in Shopify)
- DSers: import to Import List, pick the US-shipping variant(s), push to Shopify. Check it is mapped to that supplier.
- Shopify cleanup, matching the existing products:
  - Title: short and plain, like the current ones ("Stainless steel fountain, 3.2 L").
  - Description: store voice, honest, bullet specs (size, material, care). Say "Ships from the USA", never "warehouse".
    No AliExpress sold counts, no fake reviews, no health claims, no "we test every product".
  - Photos: supplier photos only, best first, remove duplicates/text-heavy ones; alt text set.
  - Product type = category (Water, Grooming, Sleep, Climb, Play, Litter) and tag = category name so the smart
    collections pick it up. Vendor "Lapwell". Inventory not tracked. Weight set if known.
  - SEO title + description. Price set; no fake compare-at prices.
  - Status ACTIVE, published to Online Store and Google & YouTube.
- Never touch the kits' bundle components unless a component changes. Don't push the 12 mapping listings in DSers.

## 5. Polish pass (every run)
- Open the storefront (www.getlapwell.com): home, each collection, every new product page, cart. Check photos load,
  prices match, nothing broken, no leftover supplier text, links work, mobile layout OK.
- Admin: no stray drafts created by DSers, collections correct, Google & YouTube product status, any Shopify warnings.
- Orders: if a real order came in, notify the store owner (don't place or pay DSers orders without the store owner).
- Update LIVE_STATE.md (product table) and this log.

## Limits
- No spending (no paid apps, ads, samples) without the store owner. No account creation, passwords or payment details.
- Don't change prices of existing products or remove products without telling the owner, except to stop a loss
  (cost went above price): then set the product to draft and report it.

