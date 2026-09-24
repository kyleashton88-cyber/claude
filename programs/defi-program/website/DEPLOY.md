# Sales website: On-Chain Operator Program

`index.html` + `media/` is the complete sales page, with the main VSL (`media/vsl-main.mp4`, 3:36, web-optimised,
click-to-play with sound, captions in `media/vsl-main.vtt`) embedded in the hero.

## Put it on Whop
- **With Whop AI:** attach `index.html` (it's in `WHOP-AI-UPLOAD.zip` as `11-website-index.html.txt`) and follow item 4
  of the build prompt: it builds the page on Whop with the VSL as the hero video.
- **Listing video:** also upload `../video/vsl-main.mp4` as the product's listing video, so the VSL plays on the Whop
  store page itself.
- **Hosting the HTML as-is:** upload the whole `website/` folder (keep `media/` next to `index.html`) to any static host
  and link the page from Whop.

## Set the application link
Every Apply button goes to "How to join" until the application form exists. Then rebuild with the real link:
`cd ../export && APPLY_URL="https://your-application-form" node build_website.js`

Rebuilding also refreshes the web VSL whenever `video/vsl-main.mp4` is re-rendered.
