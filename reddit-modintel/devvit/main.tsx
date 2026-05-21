import { Devvit } from "@devvit/public-api";
import { TLDRPanel } from "./components/TLDRPanel.js";
import { SimilarityPanel } from "./components/SimilarityPanel.js";

Devvit.configure({
  redditAPI: true,
  fetch: true,
});

Devvit.addMenuItem({
  label: "ModIntel: TLDR this post",
  location: "post",
  onPress: async (event, context) => {
    const post = await context.reddit.getPostById(event.targetId);
    const text = post.title + "\n\n" + (post.selfText || "");
    context.ui.showForm(TLDRPanel, { text });
  },
});

Devvit.addMenuItem({
  label: "ModIntel: Check Similarity",
  location: "post",
  onPress: async (event, context) => {
    const post = await context.reddit.getPostById(event.targetId);
    const text = post.title + "\n\n" + (post.selfText || "");
    context.ui.showForm(SimilarityPanel, { text });
  },
});

export default Devvit;